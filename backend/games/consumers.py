import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .managers import GroupManager

class GameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_manager = GroupManager()
        self.game_manager = None
        self.group_id = None
        self.group_name = None

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        try:
            self.group_id = self.group_manager.get_or_create_group()
            self.game_manager = self.group_manager.get_game_manager(self.group_id)
            self.group_name = self.group_manager.get_game_group_name(self.group_id)

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            
            await self.accept()
            
            await self.game_manager.handle_player_connect(
                self.group_name,
                self.channel_name,
                self.scope["user"].username
            )
            
        except Exception as e:
            print(f"Error in connect: {e}")
            await self.close()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            await self.game_manager.handle_message(self.channel_name, data)
        except Exception as e:
            print(f"Error in receive: {e}")

    async def disconnect(self, close_code):
        """연결 종료 처리"""
        try:
            if self.game_manager:
                await self.game_manager.handle_player_disconnect(self.channel_name)
            
            if self.group_id:
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception as e:
            print(f"Error in disconnect: {e}")

    # 메시지 핸들러들
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