from django.urls import re_path
from games.consumers import GameConsumer
from users.consumers import StatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/onetoone/$", GameConsumer.as_asgi()),   # 1:1 매치
    re_path(r"ws/tournament/$", GameConsumer.as_asgi()), # 토너먼트
    re_path(r"ws/status/$", StatusConsumer.as_asgi()),    # 실시간 유저 상태확인
]
