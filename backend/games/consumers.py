import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
import asyncio
from django.db import transaction
from channels.db import database_sync_to_async
from .models import Match
from users.models import User
from .group_manager import GroupManager

class GameConsumer(AsyncWebsocketConsumer):
    group_manager = GroupManager() # 그룹 관리 매니저
    connected_clients = {} # 연결된 유저
    game_states = {} # 게임 상태
    game_started = {} # 게임이 시작한지 여부
    player_sides = {} # 플레이어의 위치(왼쪽, 오른쪽)
    player_nickname = {} # 플레이어 닉네임
    game_start_times = {}  # 게임 시작 시간
    game_ended_flags = {}  # 게임 종료 상태를 저장하는 딕셔너리
    game_loop_tasks = {}

    async def connect(self):
        # 새 그룹을 생성하거나 기존 그룹에 참여
        self.group_id, group_info = self.group_manager.get_or_create_group()
        self.game_group_name = self.group_manager.get_game_group_name(self.group_id)

        # 그룹의 사용자 목록 업데이트
        self.group_manager.add_client_to_group(self.group_id, self.channel_name)

        # 채널을 그룹에 추가
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        # 게임 시작한 그룹이 아니라면 게임 상태 초기화
        if self.game_group_name not in self.connected_clients:
            self.connected_clients[self.game_group_name] = []
            self.game_states[self.game_group_name] = {
                'ball': {'x': 400, 'y': 300, 'dx': 5, 'dy': 5, 'radius': 10},
                'paddle1': {'x': 10, 'y': 250, 'width': 10, 'height': 100},
                'paddle2': {'x': 780, 'y': 250, 'width': 10, 'height': 100},
                'score': {'player1': 0, 'player2': 0}
            }
            self.game_started[self.game_group_name] = False
            self.player_sides[self.game_group_name] = {}

        # 로그인된 사용자 가져오기
        user = self.scope["user"]
        if self.game_group_name not in self.player_nickname:
             self.player_nickname[self.game_group_name] = {}

        if user.is_authenticated:
              nickname = user.username
              self.player_nickname[self.game_group_name][self.channel_name] = nickname
        else:
            await self.close()

		# 사용자 위치 설정
        if len(self.connected_clients[self.game_group_name]) == 0:
            self.player_side = 'left'
            self.player_number = 1
        else:
            self.player_side = 'right'
            self.player_number = 2

        self.connected_clients[self.game_group_name].append(self.channel_name)
        self.player_sides[self.game_group_name][self.channel_name] = {
            'side': self.player_side,
            'player': self.player_number
        }

        await self.accept()
        
        # 두 번째 사용자가 연결되면 게임 시작
        if self.game_started[self.game_group_name] == False and len(self.group_manager.get_group_info(self.group_id)['clients']) == 2:
            self.group_manager.set_group_started(self.group_id, True)
            self.game_started[self.game_group_name] = True
            self.game_start_times[self.game_group_name] = timezone.now()
            await self.start_game()

    async def start_game(self):
        player1_channel = self.connected_clients[self.game_group_name][0]
        player2_channel = self.connected_clients[self.game_group_name][1]

        player1_info = self.player_sides[self.game_group_name][player1_channel]
        player2_info = self.player_sides[self.game_group_name][player2_channel]

        player1_nickname = self.player_nickname[self.game_group_name][player1_channel]
        player2_nickname = self.player_nickname[self.game_group_name][player2_channel]
        
        game_state = self.game_states[self.game_group_name]

        # 첫 번째 사용자에게 메시지 전송
        await self.channel_layer.send(
            player1_channel,
            {
                'type': 'game_start_message',
                'state': game_state,
                'side': player1_info['side'],
                'player': player1_info['player'],
                'player1Nickname': player1_nickname,
                'player2Nickname': player2_nickname
            }
        )

        # 두 번째 사용자에게 메시지 전송
        await self.channel_layer.send(
            player2_channel,
            {
                'type': 'game_start_message',
                'state': game_state,
                'side': player2_info['side'],
                'player': player2_info['player'],
                'player1Nickname': player2_nickname,
                'player2Nickname': player1_nickname
            }
        )
        
        self.game_loop_tasks[self.game_group_name] = asyncio.create_task(self.game_loop())

    async def game_start_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameStart',
            'state': event['state'],
            'side': event['side'],
            'player': event['player'],
            'player1Nickname': event['player1Nickname'],
            'player2Nickname': event['player2Nickname']
        }))

    async def game_loop(self):
        try:
            while True:
                if self.game_group_name not in self.game_started or not self.game_started[self.game_group_name]:
                    return

                if self.game_group_name not in self.connected_clients or len(self.connected_clients[self.game_group_name]) < 2:
                    return
            
                game_state = self.game_states[self.game_group_name]
                self.update_game_state(game_state)
            
                await self.send_game_state_to_group()
                await asyncio.sleep(1/60)  # 60 FPS
        except asyncio.CancelledError:
            return


    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'move':
            await self.handle_move(data)
        if data['type'] == 'disconnect':
            if self.game_group_name in self.game_started:
                self.game_started[self.game_group_name] = False  # 게임 상태를 종료로 설정
    
            # game_loop 태스크 취소
            if self.game_group_name in self.game_loop_tasks:
                self.game_loop_tasks[self.game_group_name].cancel()
                del self.game_loop_tasks[self.game_group_name]
    
            for client in self.connected_clients[self.game_group_name]:
                await self.channel_layer.send(
                    client,
                    {
                        'type': 'opponent_disconnected_message',
                        'message': 'Opponent has disconnected. Returning to main screen.',
                        'disconnect_client': True,
                    }
                )
    
            # 그룹 정리
            await self.cleanup_group()

    async def handle_move(self, data):
        if self.game_started[self.game_group_name] == False:
            return

        game_state = self.game_states[self.game_group_name]
        if data['player'] == 1:
            paddle = game_state['paddle1']
        else:
            paddle = game_state['paddle2']
        
        if data['direction'] == 'up':
            paddle['y'] = max(0, paddle['y'] - 10)
        elif data['direction'] == 'down':
            paddle['y'] = min(500, paddle['y'] + 10)

        await self.send_game_state_to_group()

    async def disconnect(self, close_code):
        if self.group_id in self.group_manager.groups:
            group_info = self.group_manager.get_group_info(self.group_id)
            if self.channel_name in group_info['clients']:
                self.group_manager.remove_client_from_group(self.group_id, self.channel_name)

            # 상대방에게 연결이 끊겼음을 알림
            if len(group_info['clients']) == 1:
                remaining_client_channel = group_info['clients'][0]
                await self.channel_layer.send(
                    remaining_client_channel,
                    {
                        'type': 'opponent_disconnected_message',
                        'message': 'Opponent has disconnected. Returning to main screen.',
                        'disconnect_client': True,
                    }
                )
                # 게임을 종료함
                self.group_manager.set_group_started(self.group_id, False)

            await self.channel_layer.group_discard(
                self.game_group_name,
                self.channel_name
            )

            # 모든 사용자가 나가면 그룹 삭제
            if not group_info['clients']:
                self.group_manager.delete_group(self.group_id)
        else:
            return

    async def opponent_disconnected_message(self, event):
        if self.game_group_name in self.game_started and self.game_started[self.game_group_name] == False:
            return
        try:
            await self.send(text_data=json.dumps({
                'type': 'opponentDisconnected',
                'message': event['message']
            }))
        except Exception as e:
            return

        if event.get('disconnect_client', True):
            await self.close()

	
    async def end_game(self, game_state):
        # 이미 게임이 종료됐는지 확인
        if self.game_ended_flags.get(self.game_group_name, False):
            return

		# 종료 플래그 설정
        self.game_ended_flags[self.game_group_name] = True

        if game_state['score']['player1'] >= 5:
            winner = 1
        elif game_state['score']['player2'] >= 5:
            winner = 2
        else:
            winner = None

        # 그룹의 모든 유저에게 게임 끝 메시지 전송
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_end_message',
                'winner': winner
            }
        )

        if self.game_group_name in self.game_started and self.game_started[self.game_group_name] == True and winner in [1,2]:
		    # Match 모델에 데이터 저장
            player1_channel = self.connected_clients[self.game_group_name][0]
            player2_channel = self.connected_clients[self.game_group_name][1]
        
            player1_nickname = self.player_nickname[self.game_group_name][player1_channel]
            player2_nickname = self.player_nickname[self.game_group_name][player2_channel]
            
            match_start_time = self.game_start_times.get(self.game_group_name, timezone.now())
            
            match_type = 'onetoone'
            
            if winner == 1:
                match_result = 'user1_win'
            else:
                match_result = 'user2_win'
            
            await self.save_match_to_db(
                player1_nickname, 
                player2_nickname, 
                match_result, 
                game_state['score']['player1'], 
                game_state['score']['player2'],
                match_type,
                match_start_time,
                timezone.now()  # 게임 종료 시점
            )

        # 게임 상태 변경
        self.game_started[self.game_group_name] = False

        # 각 클라이언트의 socket 연결 종료
        for channel in self.connected_clients[self.game_group_name]:
            await self.channel_layer.send(
                channel,
                {
                    'type': 'disconnect_client',
                }
            )
            
        self.cleanup_group()

    @database_sync_to_async
    def save_match_to_db(self, player1_nickname, player2_nickname, match_result, player1_score, player2_score, match_type, match_start_time, match_end_time):
        Match.objects.create(
			match_username1=User.objects.get(username=player1_nickname),
			match_username2=User.objects.get(username=player2_nickname),
			match_result=match_result,
			match_start_time=match_start_time,
			match_end_time=match_end_time,
			username1_grade=player1_score,
			username2_grade=player2_score,
			match_type=match_type
		)

    async def disconnect_client(self, event):
        await self.close()
            
    async def game_end_message(self, event):
        winner = event['winner']
        await self.send(text_data=json.dumps({
            'type': 'gameEnd',
            'winner': winner
        }))

    def update_game_state(self, game_state):
        ball = game_state['ball']
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']

        # 벽과 충돌 감지
        if ball['y'] - ball['radius'] <= 0 or ball['y'] + ball['radius'] >= 600:
            ball['dy'] = -ball['dy']

        # paddle과 충돌 감지
        if (ball['x'] - ball['radius'] <= game_state['paddle1']['x'] + game_state['paddle1']['width'] and
            game_state['paddle1']['y'] <= ball['y'] <= game_state['paddle1']['y'] + game_state['paddle1']['height']) or \
           (ball['x'] + ball['radius'] >= game_state['paddle2']['x'] and
            game_state['paddle2']['y'] <= ball['y'] <= game_state['paddle2']['y'] + game_state['paddle2']['height']):
            ball['dx'] = -ball['dx']

        # 점수 업데이트
        if ball['x'] - ball['radius'] <= 0:
            game_state['score']['player2'] += 1
            self.reset_ball(ball)
        elif ball['x'] + ball['radius'] >= 800:
            game_state['score']['player1'] += 1
            self.reset_ball(ball)
		
		# 5점 득점시 게임 종료
        if game_state['score']['player1'] >= 5 or game_state['score']['player2'] >= 5:
            asyncio.create_task(self.end_game(game_state))

    def reset_ball(self, ball):
        ball['x'] = 400
        ball['y'] = 300
        ball['dx'] = -ball['dx']
        ball['dy'] = 5 if ball['dy'] > 0 else -5

    async def send_game_state_to_group(self):
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'send_game_state',
                'state': self.game_states[self.game_group_name]
            }
        )

    async def send_game_state(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': 'gameState',
                'state': event['state']
            }))
        except Exception as e:
            return

    async def cleanup_group(self):
        # 모든 유저를 지우고, 게임 state를 초기화함
        for channel in self.connected_clients.get(self.game_group_name, []):
            await self.channel_layer.group_discard(
                self.game_group_name,
                channel
            )
        self.connected_clients.pop(self.game_group_name, None)
        self.game_states.pop(self.game_group_name, None)
        self.game_started.pop(self.game_group_name, None)
        self.player_sides.pop(self.game_group_name, None)
        if self.game_group_name in self.game_loop_tasks:
                del self.game_loop_tasks[self.game_group_name]
        self.group_manager.delete_group(self.group_id)
        

