import json
from ..managers import GroupType
from ..managers.tournament_manager import TournamentState
from .base_consumers import BaseGameConsumer

class TournamentGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament_manager = None
        self.type = GroupType.TOURNAMENT

    async def handle_user_info(self):
        try:
            # 유저 정보를 받은 후 토너먼트 그룹 설정
            self.group_id = self.group_manager.get_or_create_group(self.type)
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
        elif data['type'] == 'ready':
            # 플레이어가 결승전 준비가 되었음을 알림
            await self.tournament_manager.handle_player_ready(self.channel_name)

    async def game_start(self, event):
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
            match_group = event['match_group']
            match_id = match_group.split('_')[-1]  # 'semi0' or 'semi1'에서 추출

            # tournament_manager에게 게임 결과 전달
            await self.tournament_manager.handle_game_end(match_id, winner)

        except Exception as e:
            print(f"Error in game_end: {e}")

    async def game_opponent_disconnected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'opponentDisconnected',
            'message': event['message'],
            'state': event['state']
        }))

	# 4강 결과 전송
    async def semifinal_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'semifinalResult',
            'result': event['result'],
            'message': event['message']
        }))

		# 패자는 바로 연결 종료, 승자는 연결 유지
        if event['result'] == 'lose':
            await self.close(code=1000)

	# 결승 결과 전송
    async def final_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'finalResult',
            'result': event['result'],
            'message': event['message'],
            'round': event['round']
        }))

		# 결승전이 끝났으므로 모든 플레이어 연결 종료
        await self.close(code=1000)