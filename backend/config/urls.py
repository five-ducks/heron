from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from friends.views import FriendViewSet
from games.views import MatchViewSet
from oauth.views import OAuthViewSet, login_redirect

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.contrib import admin
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'friends', FriendViewSet, basename='friend')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'oauth', OAuthViewSet, basename='oauth')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'), # API 스키마 생성 엔드포인트
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI 뷰
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

    path('oauth/login/redirect', login_redirect, name='login42_redirect'),
]
