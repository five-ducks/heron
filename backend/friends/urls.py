from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FriendViewSet

router = DefaultRouter()
router.register(r'', FriendViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
