import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_id = f"game_{self.game_id}"

        # game group에 추가
        await self.channel_layer.group_add(
            self.game_group_id, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # game group 떠나기
        await self.channel_layer.group_discard(
            self.game_group_id, 
            self.channel_name
        )

    # WebSocket으로부터 메시지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # game group에게 메시지 보내기
        await self.channel_layer.group_send(
            self.game_group_id,
            {
                "type": "game_message",
                "message": message
            }
        )

    # game group으로부터 메시지 받기
    async def game_message(self, event):
        message = event["message"]

        # WebSocket으로 메시지 보내기
        await self.send(text_data=json.dumps(
            {
                "message": message
            }
        ))
