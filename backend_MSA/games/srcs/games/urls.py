from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet

router = DefaultRouter()
router.register(r'', MatchViewSet)

urlpatterns = [
    path('', include(router.urls))
]
