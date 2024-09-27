from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, CreateGameView

router = DefaultRouter()
router.register(r'', MatchViewSet, basename='match')

urlpatterns = [
    path('', include(router.urls)),
    path('create-game/', CreateGameView.as_view(), name='create-game'),  # 게임 생성 API 추가
]
