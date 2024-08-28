from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Friend

from .serializers import (
    FriendCreationRequestSerializer,
	FriendResponseSerializer
)

class FriendViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing friendships.
    """

    @extend_schema(
        summary="Add a new friend",
        description="Add a new friend by providing necessary details.",
        request=FriendCreationRequestSerializer,
        responses={
            201: FriendResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
        },
        tags=["Friend"]
    )
    def create(self, request):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Retrieve a list of all friends",
        description="Retrieve a list of all friends, with optional filters, sorting, and pagination.",
        parameters=[
            OpenApiParameter(name='user_id', description="Filter friends by user ID", required=False, type=int),
            OpenApiParameter(name='relation', description="Filter friends by relation status", required=False, type=str, enum=['pending', 'accepted', 'blocked']),
            OpenApiParameter(name='page', description="Page number for pagination", required=False, type=int, default=1),
            OpenApiParameter(name='limit', description="Number of results per page", required=False, type=int, default=10),
            OpenApiParameter(name='sort_by', description="Sort friends by a specific field", required=False, type=str, enum=['user_id', 'friend_user_id'], default='user_id'),
            OpenApiParameter(name='order', description="Order of sorting (ascending or descending)", required=False, type=str, enum=['asc', 'desc'], default='asc'),
        ],
        responses={
            200: FriendResponseSerializer(many=True),
            400: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
        },
        tags=["Friend"]
    )
    def list(self, request):
        # Implement your logic for filtering, sorting, and pagination here
        return Response({"message": "Invalid filter parameters"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Retrieve all friends for a specific user",
        description="Retrieve all friends associated with a specific user ID.",
        parameters=[
            OpenApiParameter(name='user_id', description="User ID to retrieve friends for", required=True, type=int),
        ],
        responses={
            200: FriendResponseSerializer(many=True),
            404: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
        },
        tags=["Friend"]
    )
    def retrieve(self, request, pk=None):
        return Response({"message": "User not found or no friends available"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a friend by ID",
        description="Update the relation status of a friend by their user ID and friend user ID.",
        parameters=[
            OpenApiParameter(name='user_id', description="The ID of the user", required=True, type=int),
            OpenApiParameter(name='friend_user_id', description="The ID of the friend user", required=True, type=int),
        ],
        request=FriendResponseSerializer,
        responses={
            200: FriendResponseSerializer,
            400: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
            404: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
        },
        tags=["Friend"]
    )
    def update(self, request, pk=None, friend_user_id=None):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Remove a friend",
        description="Remove a friend by their user ID and friend user ID.",
        parameters=[
            OpenApiParameter(name='user_id', description="The ID of the user", required=True, type=int),
            OpenApiParameter(name='friend_user_id', description="The ID of the friend user", required=True, type=int),
        ],
        responses={
            204: None,
            404: OpenApiTypes.OBJECT,  # Assuming you return an object with an error message
        },
        tags=["Friend"]
    )
    def destroy(self, request, pk=None, friend_user_id=None):
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)
