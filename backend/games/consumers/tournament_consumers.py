import json
from ..managers import GroupType
from ..managers.tournament_manager import TournamentState
from .base_consumers import BaseGameConsumer

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

    async def game_opponent_disconnected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'opponentDisconnected',
            'message': event['message']
        }))

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

    async def tournament_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'tournamentStatus',
            'round': event.get('round', 'waiting'),
            'state': event.get('state', TournamentState.WAITING),
            'players': event.get('players', []),
            'matches': event.get('matches', None)
        }))