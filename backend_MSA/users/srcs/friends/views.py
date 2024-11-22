from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Friend


class FriendViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing friendships.
    """
    pass
