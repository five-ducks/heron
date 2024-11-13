from typing import Dict, Tuple
from .game_manager import GameManager

class GroupManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.groups = {}  # group_id: {clients: [], started: False}
        self.current_group_id = 0
        self.game_managers = {}  # group_id: GameManager
    
    def get_or_create_group(self) -> Tuple[str, dict]:
        # 대기 중인 그룹 찾기
        for group_id, group_info in self.groups.items():
            if len(group_info['clients']) < 2 and not group_info['started']:
                return group_id
        
        # 대기 중인 그룹이 없으면 새 그룹 생성
        self.current_group_id += 1
        new_group_id = self.current_group_id
        self.groups[new_group_id] = {
            'clients': [],
            'started': False
        }
        # 새 그룹의 GameManager 생성
        self.game_managers[new_group_id] = GameManager()
        return new_group_id
            
    def get_group_info(self, group_id) -> dict:
        return self.groups.get(group_id, {'clients': [], 'started': False})
    
    def get_game_group_name(self, group_id) -> str:
        return f"game_{group_id}"

    def get_game_manager(self, group_id) -> 'GameManager':
        return self.game_managers.get(group_id)
    
    def set_group_started(self, group_id, started: bool):
        if group_id in self.groups:
            self.groups[group_id]['started'] = started
            
    def add_client_to_group(self, group_id, channel_name: str):
        if group_id in self.groups:
            self.groups[group_id]['clients'].append(channel_name)
    
    def remove_client_from_group(self, group_id, channel_name: str):
        if group_id in self.groups:
            self.groups[group_id]['clients'].remove(channel_name)
            # 그룹이 비었으면 GameManager도 정리
            if not self.groups[group_id]['clients']:
                self.game_managers.pop(group_id, None)
    
    def delete_group(self, group_id):
        self.groups.pop(group_id, None)
        self.game_managers.pop(group_id, None)