from django.urls import re_path

from .consumers import GameConsumer

websocket_urlpatterns = [
	re_path(r"ws/local/onetoone/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
	re_path(r"ws/local/tournament/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
	re_path(r"ws/online/onetoone/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
	re_path(r"ws/online/tournament/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
]