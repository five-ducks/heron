from django.urls import re_path
from games.consumers import OneToOneGameConsumer, TournamentGameConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/onetoone/$', OneToOneGameConsumer.as_asgi()),		# 1:1 게임
    re_path(r'ws/game/tournament/$', TournamentGameConsumer.as_asgi()),	# 토너먼트 게임
]
