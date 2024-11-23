"""
URL configuration for authManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from oauth.views import OAuthViewSet, login_redirect
from custom_auth.views import AuthViewSet
from two_fa.views import TwoFAViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.contrib import admin

authRouter = DefaultRouter()
authRouter.register(r'auth', AuthViewSet, basename='auth')

oauthRouter = DefaultRouter()
oauthRouter.register(r'oauth', OAuthViewSet, basename='oauth')
oauthRouter.register(r'2fa', TwoFAViewSet, basename='2fa')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'), # API 스키마 생성 엔드포인트
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Swagger UI 뷰
    path('auth/', include(oauthRouter.urls)),
    path('', include(authRouter.urls)),
    path('admin/', admin.site.urls),

    path('oauth/login/redirect', login_redirect, name='login42_redirect'),
]

print(urlpatterns)