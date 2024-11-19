import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..managers import GroupManager, GroupType

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