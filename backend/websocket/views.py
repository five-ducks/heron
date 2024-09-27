from rest_framework import veiwsets
from rest_framework.response import Response
from rest_framework import status
from .models import Match  # Match 모델이 있다면 임포트
import uuid

class MatchViewSet(viewsets.ViewSet):
    def list(self, request):
        # Match 모델을 사용해 게임 리스트를 가져올 때 사용하는 메서드 예시
        matches = Match.objects.all()
        return Response({'matches': matches})

class CreateGameView(APIView):
    def post(self, request, *args, **kwargs):
        # 고유한 게임 ID 생성
        game_id = str(uuid.uuid4())

        # 게임 상태 초기화 (게임에 필요한 다른 데이터가 있다면 여기에 추가 가능)
        GameConsumer.connected_clients[f'game_{game_id}'] = []
        GameConsumer.game_states[f'game_{game_id}'] = {
            'ball': {'x': 400, 'y': 300, 'dx': 5, 'dy': 5, 'radius': 10},
            'paddle1': {'x': 10, 'y': 250, 'width': 10, 'height': 100},
            'paddle2': {'x': 780, 'y': 250, 'width': 10, 'height': 100},
            'score': {'player1': 0, 'player2': 0}
        }
        GameConsumer.game_started[f'game_{game_id}'] = False
        GameConsumer.player_sides[f'game_{game_id}'] = {}

        # 게임 ID 반환
        return Response({"game_id": game_id}, status=status.HTTP_201_CREATED)