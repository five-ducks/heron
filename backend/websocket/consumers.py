import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import asyncio

class GameConsumer(AsyncWebsocketConsumer):
    connected_clients = {}
    game_states = {}
    game_started = {}
    player_sides = {}

    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        if self.game_group_name not in self.connected_clients:
            self.connected_clients[self.game_group_name] = []
            self.game_states[self.game_group_name] = {
                'ball': {'x': 400, 'y': 300, 'dx': 5, 'dy': 5, 'radius': 10},
                'paddle1': {'x': 10, 'y': 250, 'width': 10, 'height': 100},
                'paddle2': {'x': 780, 'y': 250, 'width': 10, 'height': 100},
                'score': {'player1': 0, 'player2': 0}
            }
            self.game_started[self.game_group_name] = False
            self.player_sides[self.game_group_name] = {}

        if len(self.connected_clients[self.game_group_name]) == 0:
            self.player_side = 'left'
            self.player_number = 1
        else:
            self.player_side = 'right'
            self.player_number = 2

        self.connected_clients[self.game_group_name].append(self.channel_name)
        self.player_sides[self.game_group_name][self.channel_name] = {
            'side': self.player_side,
            'player': self.player_number
        }

        await self.accept()
        
        if len(self.connected_clients[self.game_group_name]) == 2:
            self.game_started[self.game_group_name] = True
            await self.start_game()

    async def disconnect(self, close_code):
        self.connected_clients[self.game_group_name].remove(self.channel_name)
        del self.player_sides[self.game_group_name][self.channel_name]
        
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

        if len(self.connected_clients[self.game_group_name]) == 0:
            del self.connected_clients[self.game_group_name]
            del self.game_states[self.game_group_name]
            del self.game_started[self.game_group_name]
            del self.player_sides[self.game_group_name]

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'move':
            await self.handle_move(data)

    async def handle_move(self, data):
        if not self.game_started[self.game_group_name]:
            return

        game_state = self.game_states[self.game_group_name]
        paddle = game_state['paddle1'] if data['player'] == 1 else game_state['paddle2']
        
        if data['direction'] == 'up':
            paddle['y'] = max(0, paddle['y'] - 10)
        elif data['direction'] == 'down':
            paddle['y'] = min(500, paddle['y'] + 10)  # 600 (canvas height) - 100 (paddle height)

        await self.send_game_state_to_group()

    async def start_game(self):
        for channel_name in self.connected_clients[self.game_group_name]:
            player_info = self.player_sides[self.game_group_name][channel_name]
            await self.channel_layer.send(
                channel_name,
                {
                    'type': 'game_start_message',
                    'side': player_info['side'],
                    'player': player_info['player']
                }
            )
        asyncio.create_task(self.game_loop())

    async def game_start_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameStart',
            'side': event['side'],
            'player': event['player']
        }))

    async def game_loop(self):
        while self.game_started[self.game_group_name] and len(self.connected_clients[self.game_group_name]) == 2:
            game_state = self.game_states[self.game_group_name]
            self.update_game_state(game_state)
            await self.send_game_state_to_group()
            await asyncio.sleep(1/60)  # 60 FPS

    def update_game_state(self, game_state):
        ball = game_state['ball']
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']

        # Simple collision detection with walls
        if ball['y'] - ball['radius'] <= 0 or ball['y'] + ball['radius'] >= 600:
            ball['dy'] = -ball['dy']

        # Simple collision detection with paddles
        if (ball['x'] - ball['radius'] <= game_state['paddle1']['x'] + game_state['paddle1']['width'] and
            game_state['paddle1']['y'] <= ball['y'] <= game_state['paddle1']['y'] + game_state['paddle1']['height']) or \
           (ball['x'] + ball['radius'] >= game_state['paddle2']['x'] and
            game_state['paddle2']['y'] <= ball['y'] <= game_state['paddle2']['y'] + game_state['paddle2']['height']):
            ball['dx'] = -ball['dx']

        # Score update
        if ball['x'] - ball['radius'] <= 0:
            game_state['score']['player2'] += 1
            self.reset_ball(ball)
        elif ball['x'] + ball['radius'] >= 800:
            game_state['score']['player1'] += 1
            self.reset_ball(ball)

    def reset_ball(self, ball):
        ball['x'] = 400
        ball['y'] = 300
        ball['dx'] = -ball['dx']
        ball['dy'] = 5 if ball['dy'] > 0 else -5

    async def send_game_state_to_group(self):
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'send_game_state',
                'state': self.game_states[self.game_group_name]
            }
        )

    async def send_game_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'gameState',
            'state': event['state']
        }))