from typing import Dict, Optional, List
import asyncio
import random
from enum import Enum
from django.utils import timezone
from channels.layers import get_channel_layer
from .game_manager import GameManager

class TournamentState(Enum):
    WAITING = "waiting"     # 대기 중
    SEMIFINAL = "semifinal" # 4강전 진행 중
    FINAL = "final"        # 결승전 진행 중
    COMPLETED = "completed" # 토너먼트 종료

class TournamentManager:
    def __init__(self):
        self.state = TournamentState.WAITING
        self.players: List[Dict] = []  # [{channel_name, username}, ...]
        self.matches = {
            'semifinal': [],
            'final': None
        }
        self.semifinal_winners = []
        self.champion = None
        self.game_managers = {}  # match_id: GameManager
        self.channel_layer = get_channel_layer()
        self.group_name: Optional[str] = None

	# 플레이어 연결 처리
    async def handle_player_connect(self, group_name: str, channel_name: str, username: str) -> None:
       try:
           self.group_name = group_name
           
           # 플레이어 추가
           self.players.append({
               'channel_name': channel_name,
               'username': username
           })

           # 4명이 모이면 토너먼트 시작
           if len(self.players) == 4:
               await self.start_semifinal()

       except Exception as e:
           print(f"Error in handle_player_connect: {e}")

    async def start_semifinal(self) -> None:
        try:
            self.state = TournamentState.SEMIFINAL
           
            # 무작위 매칭
            players = self.players.copy()
            random.shuffle(players)

            # 두 개의 4강전 매치 생성
            self.matches['semifinal'] = [
               (players[0], players[1]),
               (players[2], players[3])
            ]

            # 각 매치에 대해
            for i, (player1, player2) in enumerate(self.matches['semifinal']):
                match_id = f"semi_{i}"
                match_group = f"{self.group_name}_match_{match_id}"
    
				# 플레이어들을 매치별 채널 그룹에 추가
                await self.channel_layer.group_add(match_group, player1['channel_name'])
                await self.channel_layer.group_add(match_group, player2['channel_name'])
                
                game_manager = GameManager(match_type='tournament')
                self.game_managers[match_id] = game_manager
                
				# 게임 매니저에 플레이어 연결
                await game_manager.handle_player_connect(
                    match_group, 
                    player1['channel_name'], 
                    player1['username']
                )
                await game_manager.handle_player_connect(
                    match_group, 
                    player2['channel_name'], 
                    player2['username']
                )

        except Exception as e:
           print(f"Error in start_semifinal: {e}")

	# 결승전 시작
    async def start_final(self) -> None:
        try:
            self.state = TournamentState.FINAL
        
            # 결승전 매치 생성
            self.matches['final'] = tuple(self.semifinal_winners)  # 4강전 승자들로 매치 생성
        
            # 결승전 게임 매니저 생성 및 설정
            match_id = "final"
            match_group = f"{self.group_name}_match_{match_id}"
        
            game_manager = GameManager(match_type='tournament')
            self.game_managers[match_id] = game_manager
        
            player1, player2 = self.matches['final']
        
            # 게임 매니저에 플레이어 연결
            await game_manager.handle_player_connect(
                match_group, 
                player1['channel_name'], 
                player1['username']
            )
            await game_manager.handle_player_connect(
                match_group, 
                player2['channel_name'], 
                player2['username']
            )

        except Exception as e:
            print(f"Error in start_final: {e}")
           
    async def handle_game_end(self, match_id: str, winner: int) -> None:
        if self.state == TournamentState.SEMIFINAL:
            await self.handle_semifinal_end(match_id, winner)
        elif self.state == TournamentState.FINAL:
            await self.handle_final_end(match_id, winner)
           
	# 4강전 게임 종료 처리
    async def handle_semifinal_end(self, match_id: str, winner: int) -> None:
        try:
            print(f"Handling semifinal end - match_id: {match_id}, winner: {winner}")
            print(f"Current matches: {self.matches['semifinal']}")

            match = self.matches['semifinal'][int(match_id)]
            winner_info = match[0] if winner == 1 else match[1]
            loser_info = match[1] if winner == 1 else match[0]
            
            # 승자는 다음 라운드로
            self.semifinal_winners.append(winner_info)
            
            # 승자/패자에게 결과 전송
            await self.channel_layer.send(
                winner_info['channel_name'],
                {
                    'type': 'semifinal_result',
                    'result': 'win',
                    'message': 'Waiting for finals'
                }
            )
            
            await self.channel_layer.send(
                loser_info['channel_name'],
                {
                    'type': 'semifinal_result',
                    'result': 'lose',
                    'message': 'Tournament ended'
                }
            )

            # 게임 매니저 정리
            game_manager = self.game_managers.pop(match_id, None)
            if game_manager:
                await game_manager.cleanup()

            # 모든 4강전이 끝났는지 확인
            if len(self.semifinal_winners) == 2:
                await self.start_final()
                
        except Exception as e:
            print(f"Error in handle_semifinal_game_end: {e}")

	# 결승전 게임 종료 처리
    async def handle_final_end(self, match_id: str, winner: int) -> None:
        try:
            match = self.matches['final']
            winner_info = match[0] if winner == 1 else match[1]
            loser_info = match[1] if winner == 1 else match[0]

            self.champion = winner_info
            self.state = TournamentState.COMPLETED

            # 우승자에게 결과 전송
            await self.channel_layer.send(
                winner_info['channel_name'],
                {
                    'type': 'final_result',
                    'result': 'win',
                    'message': 'Congratulations! You are the champion!',
                    'round': 'final'
                }
            )
            
            # 준우승자에게 결과 전송
            await self.channel_layer.send(
                loser_info['channel_name'],
                {
                    'type': 'final_result',
                    'result': 'lose',
                    'message': 'Great game! You are the runner-up!',
                    'round': 'final'
                }
            )

        except Exception as e:
            print(f"Error in handle_final_end: {e}")

	# 플레이어 비정상 종료 처리
    async def handle_player_disconnect(self, channel_name: str) -> None:
        try:
           # 연결 해제된 플레이어 찾기
           disconnected_player = next((p for p in self.players if p['channel_name'] == channel_name), None)
           if not disconnected_player:
               return

           # 현재 진행 중인 매치 찾기
           current_match = None
           current_game = None
           for match_id, game_manager in self.game_managers.items():
               if channel_name in game_manager.player_infos:
                   current_match = match_id
                   current_game = game_manager
                   break

           if current_game:
               # 상대방에게 승리 처리
               opponent_channel = next(ch for ch in current_game.player_infos.keys() if ch != channel_name)
               await self.handle_match_end(current_match, opponent_channel)

           # 다른 모든 플레이어에게 알림
           for player in self.players:
               if player['channel_name'] != channel_name:
                   await self.channel_layer.send(
                       player['channel_name'],
                       {
                           'type': 'opponent_disconnected',
                           'message': f"Player {disconnected_player['username']} has disconnected."
                       }
                   )

        except Exception as e:
           print(f"Error in handle_player_disconnect: {e}")

	# 현재 게임 매니저 반환
    def get_current_game(self, channel_name: str) -> Optional[GameManager]:
       for game_manager in self.game_managers.values():
           if channel_name in game_manager.player_infos:
               return game_manager
       return None

    async def cleanup(self) -> None:
       try:
           for game_manager in self.game_managers.values():
               await game_manager.cleanup()
           
           self.game_managers.clear()
           self.players.clear()
           self.matches = {'semifinal': [], 'final': None}
           self.winners = {'semifinal': [], 'final': None}
           self.state = TournamentState.WAITING

       except Exception as e:
           print(f"Error in cleanup: {e}")