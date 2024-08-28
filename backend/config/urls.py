from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from friends.views import FriendViewSet
from games.views import MatchViewSet, TournamentViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.contrib import admin
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'friends', FriendViewSet, basename='friend')
router.register(r'matchs', MatchViewSet, basename='match')
router.register(r'tournaments', TournamentViewSet, basename='tournament')

urlpatterns = [
    # API 스키마 생성 엔드포인트
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI 뷰
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
