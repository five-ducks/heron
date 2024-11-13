from typing import Dict, Optional, List
import asyncio
import random
from django.utils import timezone
from channels.layers import get_channel_layer
from .game_manager import GameManager

class TournamentState:
    WAITING = "waiting"      # 플레이어 대기
    SEMIFINAL = "semifinal"  # 4강전 진행
    FINAL = "final"         # 결승전 진행
    FINISHED = "finished"   # 토너먼트 종료

class TournamentManager:
    def __init__(self):
       self.state = TournamentState.WAITING
       self.players: List[Dict] = []  # [{channel_name, username}, ...]
       self.matches: Dict = {
           'semifinal': [],  # [(player1, player2), (player3, player4)]
           'final': None     # (winner1, winner2)
       }
       self.winners: Dict = {
           'semifinal': [],  # [winner1, winner2]
           'final': None     # champion
       }
       self.game_managers: Dict[str, GameManager] = {}  # match_id: GameManager
       self.channel_layer = get_channel_layer()
       self.group_name: Optional[str] = None

    async def handle_player_connect(self, group_name: str, channel_name: str, username: str) -> None:
       """플레이어 접속 처리"""
       try:
           self.group_name = group_name
           
           # 플레이어 추가
           self.players.append({
               'channel_name': channel_name,
               'username': username
           })

           # 현재 상태 브로드캐스트
           await self.broadcast_tournament_status()

           print(f"Player {username} connected. Total players: {len(self.players)}")  # debugging

           # 4명이 모이면 토너먼트 시작
           if len(self.players) == 4:
               print("Starting tournament")  # debugging
               await self.start_semifinal()

       except Exception as e:
           print(f"Error in handle_player_connect: {e}")

    async def broadcast_tournament_status(self) -> None:
        try:
            # 현재 라운드 결정
            if self.state == TournamentState.WAITING:
                current_round = "waiting"
            elif self.state == TournamentState.SEMIFINAL:
                current_round = "semifinal"
            elif self.state == TournamentState.FINAL:
                current_round = "final"
            else:
                current_round = "finished"

            status_data = {
                'type': 'tournament_status',
                'round': current_round,
                'state': self.state,
                'players': [p['username'] for p in self.players],
                'matches': {
                    'semifinal': [[(p1['username'], p2['username']) for p1, p2 in self.matches['semifinal']]],
                    'final': [self.matches['final'][0]['username'], self.matches['final'][1]['username']] if self.matches['final'] else None
                } if self.matches['semifinal'] else None
            }
        
            await self.channel_layer.group_send(self.group_name, status_data)
        except Exception as e:
            print(f"Error in broadcast_tournament_status: {e}")

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
    
               game_manager = GameManager()
               self.game_managers[match_id] = game_manager
               
               await self.channel_layer.group_add(match_group, player1['channel_name'])
               await self.channel_layer.group_add(match_group, player2['channel_name'])

               # 게임 설정
               await game_manager.handle_player_connect(match_group, player1['channel_name'], player1['username'])
               await game_manager.handle_player_connect(match_group, player2['channel_name'], player2['username'])

               # 매치 시작 알림
               await self.channel_layer.send(
					match_group,
                    {
                           'type': 'match_start',
                           'match_id': match_id,
                           'player1': player1['username'],
                           'player2': player2['username'],
                           'round': 'semifinal'
                    }
                )

           await self.broadcast_tournament_status()

       except Exception as e:
           print(f"Error in start_semifinal: {e}")

    async def handle_match_end(self, match_id: str, winner_channel: str) -> None:
       """매치 종료 처리"""
       try:
           if self.state == TournamentState.SEMIFINAL:
               # 승자 정보 찾기
               winner = next(p for p in self.players if p['channel_name'] == winner_channel)
               self.winners['semifinal'].append(winner)

               # 모든 4강전이 끝났는지 확인
               if len(self.winners['semifinal']) == 2:
                   await self.start_final()

           elif self.state == TournamentState.FINAL:
               # 우승자 저장
               winner = next(p for p in self.players if p['channel_name'] == winner_channel)
               self.winners['final'] = winner
               self.state = TournamentState.FINISHED
               
               # 토너먼트 결과 발표
               await self.announce_tournament_result()

       except Exception as e:
           print(f"Error in handle_match_end: {e}")

    async def start_final(self) -> None:
       """결승전 시작"""
       try:
           self.state = TournamentState.FINAL
           self.matches['final'] = (self.winners['semifinal'][0], self.winners['semifinal'][1])

           # 결승전 게임 매니저 생성
           match_id = "final"
           game_manager = GameManager()
           self.game_managers[match_id] = game_manager

           # 게임 설정
           match_group = f"{self.group_name}_match_{match_id}"
           winner1, winner2 = self.matches['final']
           await game_manager.handle_player_connect(match_group, winner1['channel_name'], winner1['username'])
           await game_manager.handle_player_connect(match_group, winner2['channel_name'], winner2['username'])

           # 결승전 시작 알림
           for player in [winner1, winner2]:
               await self.channel_layer.send(
                   player['channel_name'],
                   {
                       'type': 'match_start',
                       'opponent': winner2['username'] if player == winner1 else winner1['username'],
                       'round': 'final'
                   }
               )

           await self.broadcast_tournament_status()

       except Exception as e:
           print(f"Error in start_final: {e}")

    async def announce_tournament_result(self) -> None:
       """토너먼트 결과 발표"""
       try:
           tournament_summary = {
               'champion': self.winners['final']['username'],
               'semifinal_matches': [
                   [(p1['username'], p2['username']) for p1, p2 in self.matches['semifinal']]
               ],
               'final_match': [
                   self.matches['final'][0]['username'],
                   self.matches['final'][1]['username']
               ]
           }

           await self.channel_layer.group_send(
               self.group_name,
               {
                   'type': 'tournament_end',
                   'champion': self.winners['final']['username'],
                   'summary': tournament_summary
               }
           )

           # 토너먼트 결과 저장
           await self.save_tournament_result()

       except Exception as e:
           print(f"Error in announce_tournament_result: {e}")

    async def handle_player_disconnect(self, channel_name: str) -> None:
       """플레이어 연결 해제 처리"""
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

    async def save_tournament_result(self) -> None:
       """토너먼트 결과 데이터베이스 저장"""
       try:
           from ..models import Match
           from users.models import User
           from channels.db import database_sync_to_async

           @database_sync_to_async
           def save_to_db():
               champion = self.winners['final']
               runner_up = self.matches['final'][0] if self.matches['final'][1]['channel_name'] == champion['channel_name'] else self.matches['final'][1]

               champion_user = User.objects.filter(username=champion['username']).first()
               runner_up_user = User.objects.filter(username=runner_up['username']).first()

               if champion_user and runner_up_user:
                   Match.objects.create(
                       match_username1=champion_user,
                       match_username2=runner_up_user,
                       match_result='user1_win',
                       match_start_time=timezone.now(),  # 토너먼트 시작 시간 저장 필요
                       match_end_time=timezone.now(),
                       match_type='tournament'
                   )

           await save_to_db()

       except Exception as e:
           print(f"Error in save_tournament_result: {e}")

    def get_current_game(self, channel_name: str) -> Optional[GameManager]:
       """현재 진행 중인 게임 매니저 반환"""
       for game_manager in self.game_managers.values():
           if channel_name in game_manager.player_infos:
               return game_manager
       return None

    async def cleanup(self) -> None:
       """리소스 정리"""
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