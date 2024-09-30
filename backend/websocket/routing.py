from django.urls import re_path
from .consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/local/onetoone/$", GameConsumer.as_asgi()),   # 로컬 1:1 매치
    re_path(r"ws/local/tournament/$", GameConsumer.as_asgi()), # 로컬 토너먼트
    re_path(r"ws/online/onetoone/$", GameConsumer.as_asgi()),  # 온라인 1:1 매치
    re_path(r"ws/online/tournament/$", GameConsumer.as_asgi()),# 온라인 토너먼트
]
