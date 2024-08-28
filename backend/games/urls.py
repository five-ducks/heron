from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, TournamentViewSet

router = DefaultRouter()
router.register(r'', MatchViewSet, basename='match')
router.register(r'', TournamentViewSet, basename='tournament')

urlpatterns = [
    path('', include(router.urls)),
]
