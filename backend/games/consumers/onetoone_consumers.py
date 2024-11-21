import json
from ..managers import GroupType
from .base_consumers import BaseGameConsumer

class OneToOneGameConsumer(BaseGameConsumer):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.game_manager = None
       self.type = GroupType.ONETOONE

    async def handle_user_info(self):
        try:
            # 유저 정보를 받은 후 게임 그룹 설정
            self.group_id = self.group_manager.get_or_create_group(self.type)
            self.game_manager = self.group_manager.get_game_manager(self.group_id)

			# 그룹 이름 설정
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
        print(f"game_state: {event['state']}")
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
        try:
            # 게임 종료 메시지 전송
            await self.send(text_data=json.dumps({
                'type': 'gameEnd',
                'winner': event['winner']
            }))

            # 웹소켓 연결 정상 종료 (close code 1000)
            await self.close(code=1000)

        except Exception as e:
            print(f"Error in game_end: {e}")
            # 에러 발생 시에도 연결 종료 시도
            await self.close()


    async def game_opponent_disconnected(self, event):
        await self.send(text_data=json.dumps({
            'type': 'opponentDisconnected',
            'message': event['message']
        }))