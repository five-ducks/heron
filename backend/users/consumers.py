from .models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        await self.change_user_status(User.STATUS_MAP['온라인'])
        await self.accept()

    async def disconnect(self, close_code):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.change_user_status(User.STATUS_MAP['오프라인'])

    async def change_user_status(self, status):
        self.user.status = status              # 데이터베이스에 접근하여 상태 업데이트
        await sync_to_async(self.user.save)()  # sync_to_async로 비동기 실행
