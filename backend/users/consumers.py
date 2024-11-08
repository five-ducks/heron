from django.contrib.sessions.models import Session
from .models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.change_user_status(User.STATUS_MAP['오프라인'])
            await self.delete_user_session()

    @database_sync_to_async
    def delete_user_session(self):
        session_key = self.scope['session'].session_key

        if session_key:
            sessions = Session.objects.filter(session_key=session_key)
            for session in sessions:
                session.delete()

    async def change_user_status(self, status):
        self.user.status = status              # 데이터베이스에 접근하여 상태 업데이트
        await sync_to_async(self.user.save)()  # sync_to_async로 비동기 실행
