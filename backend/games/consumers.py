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
	
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            await self.handle_receive_message(data)
        except Exception as e:
            print(f"Error in receive: {e}")

    async def handle_receive_message(self, data: dict):
        raise NotImplementedError
    
    async def disconnect(self, close_code):
        try:
			# 비정상 종료시 상대방에게 알림
            if close_code != 1000:
                await self.game_manager.handle_player_disconnect(self.channel_name)
			
			# 종료 처리
            self.group_manager.group_cleanup(self.group_id, self.channel_name)

        except Exception as e:
            print(f"Error in disconnect: {e}")

class OneToOneGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.game_manager = None

    async def connect(self):
        try:
            # 1대1 게임 그룹 찾기/생성
            self.group_id = self.group_manager.get_or_create_group(GroupType.ONETOONE)
            self.game_manager = self.group_manager.get_game_manager(self.group_id)
            
			# 그룹 이름 설정
            self.group_name = f"game_{self.group_id}"

            # 채널 그룹에 추가
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            self.group_manager.add_client_to_group(self.group_id, self.channel_name)
            
            await self.accept()
            
			# 플레이어 설정
            await self.game_manager.handle_player_connect(
                self.group_name,
                self.channel_name,
                self.scope["user"].username
            )
            
        except Exception as e:
            print(f"Error in connect: {e}")
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

    async def connect(self):
        try:
            # 토너먼트 그룹 찾기/생성
           self.group_id = self.group_manager.get_or_create_group(GroupType.TOURNAMENT)
           self.tournament_manager = self.group_manager.get_tournament_manager(self.group_id)
           
		   # 그룹 이름 설정
           self.group_name = f"tournament_{self.group_id}"
           
		   # 채널 그룹에 추가
           await self.channel_layer.group_add(self.group_name, self.channel_name)
           self.group_manager.add_client_to_group(self.group_id, self.channel_name)
            
           await self.accept()
           
		   # 플레이어 추가
           await self.tournament_manager.handle_player_connect(
               self.group_name,
               self.channel_name,
               self.scope["user"].username
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

    async def match_start(self, event):
       await self.send(text_data=json.dumps({
           'type': 'matchStart',
           'match_id': event['match_id'],
           'player1': event['player1'],
           'player2': event['player2'],
           'round': event['round']
       }))
    
    async def game_start(self, event):
        """게임 시작 메시지 전송"""
        await self.send(text_data=json.dumps({
            'type': 'gameStart',
            'state': event['state'],
            'side': event['side'],
            'player': event['player'],
            'player1Nickname': event['player1Nickname'],
            'player2Nickname': event['player2Nickname']
        }))

    async def game_state(self, event):
        """게임 상태 업데이트 전송"""
        await self.send(text_data=json.dumps({
            'type': 'gameState',
            'state': event['state']
        }))

    async def game_end(self, event):
        """게임 종료 메시지 전송"""
        await self.send(text_data=json.dumps({
            'type': 'gameEnd',
            'winner': event['winner']
        }))

    async def game_opponent_disconnected(self, event):
        """상대방 연결 해제 메시지 전송"""
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