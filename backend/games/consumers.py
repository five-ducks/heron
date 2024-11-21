import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .managers import GroupManager, GroupType
from .managers.tournament_manager import TournamentState

class BaseGameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_manager = GroupManager()
        self.group_id = None
        self.group_name = None
        self.user_info = None
    
    async def connect(self):
        try:
            await self.accept()

            # 연결 성공 메시지 전송
            await self.send(text_data=json.dumps({
                'type': 'connectionSuccess',
                'message': 'WebSocket connection established'
            }))
        except Exception as e:
            print(f"Error in connect: {e}")
            await self.close()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data['type'] == 'user_info':
                # 유저 정보 저장
                self.user_info = data['user_info']

                await self.handle_user_info(self.user_info)
            await self.handle_receive_message(data)
        except Exception as e:
            print(f"Error in receive: {e}")

    async def handle_receive_message(self, data: dict):
        raise NotImplementedError
    
    async def handle_user_info(self, user_info):
        raise NotImplementedError

    async def disconnect(self, close_code):
        try:
			# 비정상 종료시 상대방에게 알림
            if close_code != 1000:
                if self.type == GroupType.ONETOONE:
                    await self.game_manager.handle_player_disconnect(self.channel_name)
                else:
                    self.type == GroupType.TOURNAMENT
                    await self.tournament_manager.handle_player_disconnect(self.channel_name)
			
			# 종료 처리
            self.group_manager.group_cleanup(self.group_id, self.channel_name)

        except Exception as e:
            print(f"Error in disconnect: {e}")

class OneToOneGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.game_manager = None
       self.type = GroupType.ONETOONE

    async def handle_user_info(self, user_info):
        try:
            # 유저 정보를 받은 후 게임 그룹 설정
            self.group_id = self.group_manager.get_or_create_group(GroupType.ONETOONE)
            self.game_manager = self.group_manager.get_game_manager(self.group_id)
            self.group_name = f"game_{self.group_id}"

            # 채널 그룹에 추가
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            self.group_manager.add_client_to_group(self.group_id, self.channel_name)

            # 플레이어 설정
            await self.game_manager.handle_player_connect(
                self.group_name,
                self.channel_name,
                self.user_info['username']
            )

        except Exception as e:
            print(f"Error in handle_user_info: {e}")
            await self.close()

    async def handle_receive_message(self, data: dict):
        if data['type'] == 'move':
            await self.game_manager.handle_message(self.channel_name, data)

    async def game_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameState',
            'state': event['state']
        }))

    async def game_start(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameStart',
            'state': event['state'],
            'side': event['side'],
            'player': event['player'],
            'player1Nickname': event['player1Nickname'],
            'player2Nickname': event['player2Nickname']
        }))

    async def game_end(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameEnd',
            'winner': event['winner']
        }))

    async def game_opponent_disconnected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'opponentDisconnected',
            'message': event['message']
        }))

class TournamentGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.tournament_manager = None
       self.type = GroupType.TOURNAMENT

    async def connect(self):
        try:
            await self.accept()
            # 토너먼트 그룹 찾기/생성

            self.group_id = self.group_manager.get_or_create_group(GroupType.TOURNAMENT)
            self.tournament_manager = self.group_manager.get_tournament_manager(self.group_id)

		    # 그룹 이름 설정
            self.group_name = f"tournament_{self.group_id}"

		    # 채널 그룹에 추가
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            self.group_manager.add_client_to_group(self.group_id, self.channel_name)

		    # 플레이어 추가
            await self.tournament_manager.handle_player_connect(
                self.group_name,
                self.channel_name,
                self.user_info['username']
            )

        except Exception as e:
            print(f"Error in connect: {e}")
            await self.close()

    async def handle_receive_message(self, data: dict):
       if data['type'] == 'move':
           # 현재 진행 중인 게임이 있다면 해당 게임 매니저에게 전달
           current_game = self.tournament_manager.get_current_game(self.channel_name)
           if current_game:
               await current_game.handle_message(self.channel_name, data)
    
    async def game_start(self, event):
        print("game_start consumer")
        print("event: ", event)
        await self.send(text_data=json.dumps({
            'type': 'gameStart',
            'state': event['state'],
            'side': event['side'],
            'player': event['player'],
            'player1Nickname': event['player1Nickname'],
            'player2Nickname': event['player2Nickname']
        }))

    async def game_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameState',
            'state': event['state']
        }))

    async def game_end(self, event):
        try:
            winner = event['winner']
            match_id = self.group_name.split('_')[-1]  # 'semi_0' or 'semi_1'에서 추출
            print("match_id: ", match_id)
            
            # tournament_manager에게 게임 결과 전달
            await self.tournament_manager.handle_game_end(match_id, winner)

        except Exception as e:
            print(f"Error in game_end: {e}")

	# 4강 결과 전송
    async def semifinal_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'semifinalResult',
            'result': event['result'],    # 'win' 또는 'lose'
            'message': event['message'],
            'nextRound': 'final' if event['result'] == 'win' else 'exit'  # 다음 라운드 정보
        }))

	# 결승 결과 전송
    async def final_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'finalResult',
            'result': event['result'],
            'message': event['message'],
            'round': event['round'],
            'nextRound': 'complete'
        }))

	# 토너먼트 종료
    async def tournament_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tournamentResult',
            'champion': event['champion'],
            'message': event['message']
        }))

    async def game_opponent_disconnected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'opponentDisconnected',
            'message': event['message']
        }))

    async def tournament_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tournamentStatus',
            'round': event.get('round', 'waiting'),
            'state': event.get('state', TournamentState.WAITING),
            'players': event.get('players', []),
            'matches': event.get('matches', None)
        }))

    async def game_state(self, event):
       await self.send(text_data=json.dumps({
           'type': 'gameState',
           'state': event['state']
       }))

    async def match_end(self, event):
       await self.send(text_data=json.dumps({
           'type': 'matchEnd',
           'winner': event['winner'],
           'nextMatch': event.get('nextMatch')
       }))
    
    async def tournament_end(self, event):
       """토너먼트 종료 메시지 전송"""
       await self.send(text_data=json.dumps({
           'type': 'tournamentEnd',
           'champion': event['champion'],
           'summary': event['summary']
       }))

    async def tournament_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tournamentResult',
            'champion': event['champion']
        }))

    async def opponent_disconnected(self, event):
       """상대방 연결 해제 메시지 전송"""
       await self.send(text_data=json.dumps({
           'type': 'opponentDisconnected',
           'message': event['message']
       }))