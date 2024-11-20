from typing import Dict, Optional, List
import random
from enum import Enum
from channels.layers import get_channel_layer
from .game_manager import GameManager

class TournamentState(Enum):
    WAITING = "waiting"     		# 대기 중
    SEMIFINAL = "semifinal" 		# 4강전 진행 중
    SEMIFINAL_END = "semifinal_end"	# 4강전 종료
    FINAL = "final"					# 결승전 진행 중
    FINISH = "finish"				# 토너먼트 종료

class TournamentManager:
    def __init__(self):
        self.state = TournamentState.WAITING
        self.players: List[Dict] = []  # [{channel_name, username, ready}, ...]
        self.matches = {
            'semifinal': [],
            'final': None
        }
        self.semifinal_winners = []
        self.semifinal_losers = set()
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
           
	# 결승 준비 완료 처리
    async def handle_player_ready(self, channel_name: str) -> None:
        try:
            if self.state != TournamentState.SEMIFINAL_END:
                return

            # 준비 완료 상태
            for winner in self.semifinal_winners:
                if winner['channel_name'] == channel_name:
                    winner['ready'] = True
                    break

            # 모든 승자가 준비되었는지 확인
            if all(winner.get('ready', False) for winner in self.semifinal_winners):
                await self.start_final()

        except Exception as e:
            print(f"Error in handle_player_ready: {e}")

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
                match_id = f"semi{i}"
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
            self.matches['final'] = tuple(self.semifinal_winners)

            match_id = "final"
            match_group = f"{self.group_name}_match_{match_id}"
            final_waiting_group = f"{self.group_name}_final_waiting"

            player1, player2 = self.matches['final']

            # 결승 대기 그룹에서 결승전 매치 그룹으로 이동
            for player in (player1, player2):
                await self.channel_layer.group_discard(final_waiting_group, player['channel_name'])
                await self.channel_layer.group_add(match_group, player['channel_name'])

            game_manager = GameManager(match_type='tournament')
            self.game_managers[match_id] = game_manager

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
            # 이미 처리된 매치인지 확인
            if match_id not in self.game_managers:
                return

            await self.handle_semifinal_end(match_id, winner)

        elif self.state == TournamentState.FINAL:
            await self.handle_final_end(match_id, winner)

	# 4강전 게임 종료 처리
    async def handle_semifinal_end(self, match_id: str, winner: int) -> None:
        try:
            match_index = int(match_id[-1]) 
            match = self.matches['semifinal'][match_index]

            winner_info = match[0] if winner == 1 else match[1]
            loser_info = match[1] if winner == 1 else match[0]

			# 승자와 패자 정보 저장
            self.semifinal_winners.append(winner_info)
            self.semifinal_losers.add(loser_info['channel_name'])
            
			# 승자를 결승전 대기 그룹으로 이동
            final_waiting_group = f"{self.group_name}_final_waiting"
            await self.channel_layer.group_add(final_waiting_group, winner_info['channel_name'])

            # 승자에게 결과 전송
            await self.channel_layer.send(
                winner_info['channel_name'],
                {
                    'type': 'semifinal_result',
                    'result': 'win',
                    'message': 'READY',
                }
            )

            # 패자에게 결과 전송
            await self.channel_layer.send(
                loser_info['channel_name'],
                {
                    'type': 'semifinal_result',
                    'result': 'lose',
                    'message': 'EXIT'
                }
            )

            # 게임 매니저 정리
            game_manager = self.game_managers.pop(match_id, None)
            if game_manager:
                await game_manager.cleanup()

            # 모든 4강전이 끝났는지 확인
            if len(self.semifinal_winners) == 2:
                self.state = TournamentState.SEMIFINAL_END

        except Exception as e:
            print(f"Error in handle_semifinal_game_end: {e}")

	# 결승전 게임 종료 처리
    async def handle_final_end(self, match_id: str, winner: int) -> None:
        try:
            match = self.matches['final']
            winner_info = match[0] if winner == 1 else match[1]
            loser_info = match[1] if winner == 1 else match[0]

            self.champion = winner_info
            self.state = TournamentState.FINISH

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
            # 정상 종료된 플레이어면 추가 처리하지 않음
            if channel_name in self.semifinal_losers:
                self.semifinal_losers.remove(channel_name)
                return

            # 4강전 승자인 경우 추가 처리하지 않음
            if self.state == TournamentState.SEMIFINAL_END and \
               any(winner['channel_name'] == channel_name for winner in self.semifinal_winners):
                return

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
                            'type': 'game_opponent_disconnected',
                            'message': f"Player {disconnected_player['username']} has disconnected."
                        }
                    )

        except Exception as e:
           print(f"Error in handle_player_disconnect: {e}")

	# 상대방이 종료했을 때 승리 처리
    async def handle_match_end(self, match_id: str, winner_channel: str) -> None:
        try:
            if match_id.startswith('semi'):
                # 4강전인 경우
                game_manager = self.game_managers.get(match_id)
                if game_manager:
                    # 승리자의 플레이어 번호 찾기 (1 또는 2)
                    winner_number = 1 if list(game_manager.player_infos.keys())[0] == winner_channel else 2
                    
                    # 게임 매니저에서 정리
                    self.game_managers.pop(match_id, None)
                    await game_manager.cleanup()
                    
                    # 4강전 결과 처리
                    await self.handle_semifinal_end(match_id, winner_number)
                    
            elif match_id == 'final':
                # 결승전인 경우
                game_manager = self.game_managers.get(match_id)
                if game_manager:
                    # 승리자의 플레이어 번호 찾기 (1 또는 2)
                    winner_number = 1 if list(game_manager.player_infos.keys())[0] == winner_channel else 2
                    
                    # 게임 매니저에서 정리
                    self.game_managers.pop(match_id, None)
                    await game_manager.cleanup()
                    
                    # 결승전 결과 처리
                    await self.handle_final_end(match_id, winner_number)
        
        except Exception as e:
            print(f"Error in handle_match_end: {e}")
	
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