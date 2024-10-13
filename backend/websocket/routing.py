from django.urls import re_path
from games.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/onetoone/$", GameConsumer.as_asgi()),   # 1:1 매치
    re_path(r"ws/tournament/$", GameConsumer.as_asgi()), # 토너먼트
]
