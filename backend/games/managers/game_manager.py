from typing import Dict, Optional, Tuple
import asyncio
from django.utils import timezone
from channels.layers import get_channel_layer
from ..elements import GameState

class GameManager:
    def __init__(self):
        # 기본 속성 초기화
        self.game_state: GameState = None
        self.player_infos: Dict[str, Dict] = {}  # channel_name: player_info
        self.game_loop_task: Optional[asyncio.Task] = None
        self.game_start_time: Optional[timezone.datetime] = None
        self.ended_flag: bool = False
        self.channel_layer = get_channel_layer()
        self.group_name: Optional[str] = None

    def initialize_game(self) -> None:
        """게임 상태 초기화"""
        self.game_state = GameState()
        self.ended_flag = False
            
    def add_player_info(self, channel_name: str, player_info: dict) -> None:
        """플레이어 정보 추가"""
        self.player_infos[channel_name] = player_info

    def get_game_state(self) -> Optional[GameState]:
        """현재 게임 상태 반환"""
        return self.game_state

    def get_player_info(self, channel_name: str) -> dict:
        """특정 플레이어 정보 반환"""
        return self.player_infos.get(channel_name, {})

    def get_all_player_infos(self, clients: list) -> Tuple[Optional[dict], Optional[dict]]:
        """모든 플레이어 정보 반환"""
        try:
            player1_info = self.player_infos[clients[0]]
            player2_info = self.player_infos[clients[1]]
            return player1_info, player2_info
        except (IndexError, KeyError):
            return None, None

    def set_game_loop_task(self, task: asyncio.Task) -> None:
        """게임 루프 태스크 설정"""
        self.game_loop_task = task

    async def handle_player_connect(self, group_name: str, channel_name: str, username: str) -> None:
        """신규 플레이어 접속 처리"""
        try:
            self.group_name = group_name
            
            # 플레이어 정보 설정
            is_first_player = len(self.player_infos) == 0
            player_info = {
                'number': 1 if is_first_player else 2,
                'side': 'left' if is_first_player else 'right',
                'nickname': username
            }
            self.add_player_info(channel_name, player_info)

            # 두 명이 모이면 게임 시작
            if len(self.player_infos) == 2:
                await self.start_game()
        except Exception as e:
            print(f"Error in handle_player_connect: {e}")
            raise

    async def handle_message(self, channel_name: str, message: dict) -> None:
        """플레이어로부터 받은 메시지 처리"""
        try:
            if message['type'] == 'move':
                await self.handle_move(channel_name, message)
            elif message['type'] == 'disconnect':
                await self.handle_player_disconnect(channel_name)
        except Exception as e:
            print(f"Error in handle_message: {e}")

    async def handle_move(self, channel_name: str, data: dict) -> None:
        """플레이어 이동 처리"""
        try:
            if not self.game_state or self.ended_flag:
                return

            player_info = self.get_player_info(channel_name)
            if not player_info:
                return

            paddle = (self.game_state.paddle1 
                     if player_info['number'] == 1 
                     else self.game_state.paddle2)
            
            if data['direction'] == 'up':
                paddle.y = max(0, paddle.y - 10)
            elif data['direction'] == 'down':
                paddle.y = min(500, paddle.y + 10)

            await self.broadcast_game_state()
        except Exception as e:
            print(f"Error in handle_move: {e}")

    async def start_game(self) -> None:
        """게임 시작"""
        try:
            self.initialize_game()
            self.game_start_time = timezone.now()
            
            # 각 플레이어에게 시작 메시지 전송
            clients = list(self.player_infos.keys())
            player1_info, player2_info = self.get_all_player_infos(clients)
            
            for channel_name, player_info in self.player_infos.items():
                await self.channel_layer.send(
                    channel_name,
                    {
                        'type': 'game_start',
                        'state': self.game_state.to_dict(),
                        'side': player_info['side'],
                        'player': player_info['number'],
                        'player1Nickname': player1_info['nickname'],
                        'player2Nickname': player2_info['nickname']
                    }
                )
            
            # 게임 루프 시작
            self.game_loop_task = asyncio.create_task(self.run_game_loop())
        except Exception as e:
            print(f"Error in start_game: {e}")
            raise

    async def run_game_loop(self) -> None:
        """게임 루프 실행"""
        try:
            while True:
                if not self.game_state:
                    break

                self.game_state.update()
                
                if self.game_state.is_game_over():
                    await self.end_game()
                    break
                
                await self.broadcast_game_state()
                await asyncio.sleep(1/60)  # 60 FPS
        except asyncio.CancelledError:
            print("Game loop cancelled")
            return
        except Exception as e:
            print(f"Error in game_loop: {e}")

    async def end_game(self) -> None:
        """게임 종료 처리"""
        try:
            if self.ended_flag:
                return

            self.ended_flag = True
            winner = self.game_state.get_winner()

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'game_end',
                    'winner': winner
                }
            )

            await self.save_match_result()
        except Exception as e:
            print(f"Error in end_game: {e}")

    async def handle_player_disconnect(self, channel_name: str) -> None:
        """플레이어 연결 해제 처리"""
        try:
            if channel_name in self.player_infos:
                # 다른 플레이어에게 알림
                for other_channel in self.player_infos:
                    if other_channel != channel_name:
                        await self.channel_layer.send(
                            other_channel,
                            {
                                'type': 'game_opponent_disconnected',
                                'message': 'Opponent has disconnected.'
                            }
                        )
                
                # 플레이어 정보 제거
                self.player_infos.pop(channel_name, None)
                await self.cleanup()
        except Exception as e:
            print(f"Error in handle_player_disconnect: {e}")

    async def broadcast_game_state(self) -> None:
        """현재 게임 상태를 모든 플레이어에게 전송"""
        try:
            if self.game_state:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'game_state',
                        'state': self.game_state.to_dict()
                    }
                )
        except Exception as e:
            print(f"Error in broadcast_game_state: {e}")

    async def save_match_result(self) -> None:
        """게임 결과를 데이터베이스에 저장"""
        try:
            if not self.game_state or not self.game_start_time:
                return

            from ..models import Match
            from users.models import User
            from channels.db import database_sync_to_async

            clients = list(self.player_infos.keys())
            player1_info, player2_info = self.get_all_player_infos(clients)

            if not player1_info or not player2_info:
                return

            @database_sync_to_async
            def save_to_db():
                try:
                    user1 = User.objects.filter(username=player1_info['nickname']).first()
                    user2 = User.objects.filter(username=player2_info['nickname']).first()

                    if user1 and user2:
                        Match.objects.create(
                            match_username1=user1,
                            match_username2=user2,
                            match_result='user1_win' if self.game_state.get_winner() == 1 else 'user2_win',
                            match_start_time=self.game_start_time,
                            match_end_time=timezone.now(),
                            username1_grade=self.game_state.score.player1,
                            username2_grade=self.game_state.score.player2,
                            match_type='onetoone'
                        )
                except Exception as e:
                    print(f"Error in save_to_db: {e}")

            await save_to_db()
        except Exception as e:
            print(f"Error in save_match_result: {e}")

    async def cleanup(self) -> None:
        """리소스 정리"""
        try:
            if self.game_loop_task:
                self.game_loop_task.cancel()
                self.game_loop_task = None

            self.game_state = None
            self.player_infos.clear()
            self.ended_flag = False
            self.game_start_time = None
        except Exception as e:
            print(f"Error in cleanup: {e}")