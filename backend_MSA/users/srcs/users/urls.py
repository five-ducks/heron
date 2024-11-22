from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExternalUserViewSet

externalRouter = DefaultRouter()
externalRouter.register(r'users', ExternalUserViewSet, basename='external-user')

urlpatterns = [
    path('', include(externalRouter.urls))
]