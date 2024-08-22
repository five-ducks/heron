from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/friends/', UserViewSet.as_view({'get': 'friends'}), name='user-friends')
]
