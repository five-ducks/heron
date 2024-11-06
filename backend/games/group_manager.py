from uuid import uuid4

class GroupManager:
    def __init__(self):
        self.groups = {}

    def get_or_create_group(self):
        available_group = None

        # 대기 중인 그룹 확인
        for group_id, info in self.groups.items():
            if not info['started']:
                available_group = group_id
                break

        if not available_group:
            new_group_id = str(uuid4())
            self.groups[new_group_id] = {
                'clients': [],
                'started': False,
                'game_group_name': f'game_{new_group_id}'
            }
            return new_group_id, self.groups[new_group_id]

        return available_group, self.groups[available_group]

    def get_group_info(self, group_id):
        return self.groups[group_id]

    def get_game_group_name(self, group_id):
        if group_id in self.groups:
            return self.groups[group_id]['game_group_name']
        return None

    def add_client_to_group(self, group_id, client):
        if group_id in self.groups:
            self.groups[group_id]['clients'].append(client)

    def remove_client_from_group(self, group_id, client):
        if group_id in self.groups and client in self.groups[group_id]['clients']:
            self.groups[group_id]['clients'].remove(client)

    def set_group_started(self, group_id, started):
        if group_id in self.groups:
            self.groups[group_id]['started'] = started

    def delete_group(self, group_id):
        if group_id in self.groups:
            del self.groups[group_id]