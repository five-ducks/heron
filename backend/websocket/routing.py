from django.urls import re_path
from games.consumers import OneToOneGameConsumer, TournamentGameConsumer
from users.consumers import StatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/onetoone/$', OneToOneGameConsumer.as_asgi()),		# 1:1 게임
    re_path(r'ws/tournament/$', TournamentGameConsumer.as_asgi()),	# 토너먼트 게임
    re_path(r"ws/status/$", StatusConsumer.as_asgi()),    # 실시간 유저 상태확인
]
