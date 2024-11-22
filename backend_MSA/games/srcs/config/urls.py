from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import MatchViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin

router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='match')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('games/', include(router.urls)),
    path('admin/', admin.site.urls),
]
