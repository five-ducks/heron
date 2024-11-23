from .models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        # websocket 연결을 시도했을때 로그인된 상태라면 연결을 수락 / 그렇지 않으면 연결을 끊음
        if not isinstance(self.user, AnonymousUser):
            await self.change_user_status(User.STATUS_MAP['온라인'])
            await self.accept()
        else:
            await self.close()
        
    async def disconnect(self, close_code):
        self.user = self.scope['user']
    
        if not isinstance(self.user, AnonymousUser):
            try:
                await sync_to_async(self.user.refresh_from_db)()
                await self.change_user_status(User.STATUS_MAP['오프라인'])
            except self.user.DoesNotExist:
                pass

    async def change_user_status(self, status):
        self.user.status = status
        await sync_to_async(self.user.save)()
