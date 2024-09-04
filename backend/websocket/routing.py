from django.urls import re_path

from .consumers import GameConsumer

websocket_urlpatterns = [
	re_path(r"ws/game/onetoone/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
	re_path(r"ws/game/tournament/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
]