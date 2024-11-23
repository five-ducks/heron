from django.urls import re_path
from users.consumers import StatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/status/$", StatusConsumer.as_asgi()),    # 실시간 유저 상태확인
]
