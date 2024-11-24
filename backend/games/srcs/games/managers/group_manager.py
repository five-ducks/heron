from channels.layers import get_channel_layer
from typing import Optional
from .game_manager import GameManager
from .tournament_manager import TournamentManager
from enum import Enum
import uuid

class GroupType(Enum):
    ONETOONE = "onetoone"
    TOURNAMENT = "tournament"

class GroupManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.channel_layer = get_channel_layer()
            cls._instance._groups = {}  # group_id: group_info
            cls._instance._game_managers = {}  # group_id: GameManager (1대1용)
            cls._instance._tournament_managers = {}  # group_id: TournamentManager (토너먼트용)
        return cls._instance

    def get_or_create_group(self, group_type: GroupType) -> str:
        # 참여 가능한 기존 그룹 찾기
        for group_id, group_info in self._groups.items():
            if (group_info['type'] == group_type and not group_info['started']):
                if ((group_type == GroupType.ONETOONE and len(group_info['clients']) < 2) or
                    (group_type == GroupType.TOURNAMENT and len(group_info['clients']) < 4)):
                    return group_id

        # 새 그룹 생성
        new_group_id = str(uuid.uuid4())
        self._groups[new_group_id] = {
            'type': group_type,
            'clients': [],
            'started': False
        }

        # 그룹 타입에 따른 매니저 생성
        if group_type == GroupType.ONETOONE:
            self._game_managers[new_group_id] = GameManager(self, match_type='onetoone')
        else:
            self._tournament_managers[new_group_id] = TournamentManager(self)

        return new_group_id

    def add_client_to_group(self, group_id: str, channel_name: str) -> None:
        if group_id in self._groups:
            self._groups[group_id]['clients'].append(channel_name)

	# 1대1 게임 매니저 반환
    def get_game_manager(self, group_id: str) -> Optional[GameManager]:
        return self._game_managers.get(group_id)

	# 토너먼트 매니저 반환
    def get_tournament_manager(self, group_id: str) -> Optional[TournamentManager]:
        return self._tournament_managers.get(group_id)

    def get_group_info(self, group_id: str) -> dict:
        return self._groups.get(group_id, {})

	# 종료
    async def group_cleanup(self, group_id: str, channel_name: str) -> None:
        group_info = self.get_group_info(group_id)
        group_name = f"game_{group_id}"

		# 채널 그룹에서 해당 유저 제거
        await self.channel_layer.group_discard(group_name, channel_name)
        
		# 그룹의 clients 목록에서 유저 제거
        if 'clients' in group_info:
            group_info['clients'].remove(channel_name)

		# 그룹에 더 이상 클라이언트가 없으면 그룹 목록에서 삭제
        if not group_info['clients']:
            game_manager = self._game_managers.pop(group_id, None)
            if game_manager:
                game_manager.cleanup()
            self._groups.pop(group_id)