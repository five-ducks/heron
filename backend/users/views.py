from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .serializers import (
    AuthTokenSerializer, 
    CreateUserRequestSerializer, 
    UserResponseSerializer, 
    LoginRequestSerializer, 
    LoginResponseSerializer
)

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing users.
    """
 
    @extend_schema(
        summary="Create a new user",
        description="Endpoint to create a new user in the system.",
        request=CreateUserRequestSerializer,
        responses={
            201: UserResponseSerializer,
            400: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    def create(self, request):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="User login",
        description="Endpoint to log in a user and return an authentication token.",
        parameters=[
            OpenApiParameter(name='user_login_id', description="The user name for login", required=True, type=str),
            OpenApiParameter(name='user_login_password', description="The password for login in clear text", required=True, type=str),
        ],
        responses={
            200: LoginResponseSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get'])
    def login(self, request):
        return Response({"message": "Invalid username/password supplied"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Unauthorized. Invalid login ID or password."}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        summary="User logout",
        description="Endpoint to log out a user and invalidate the session.",
        parameters=[
            OpenApiParameter(name='token', description="Authentication token required for logout.", required=True, type=str),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    @action(detail=False, methods=['delete'])
    def logout(self, request):
        return Response({"message": "Successful logout."}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Unauthorized. Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        summary="Get a user by ID",
        description="Endpoint to retrieve a user by their unique ID.",
        parameters=[
            OpenApiParameter(name='username', description="The ID of the user to retrieve.", required=True, type=int),
        ],
        responses={
            200: UserResponseSerializer,
            404: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    def retrieve(self, request, pk=None):
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Update a user by ID",
        description="Endpoint to update a user's information by their unique ID.",
        parameters=[
            OpenApiParameter(name='username', description="The ID of the user to update.", required=True, type=int),
        ],
        request=CreateUserRequestSerializer,
        responses={
            200: UserResponseSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    def update(self, request, pk=None):
        return Response({"message": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a user by ID",
        description="Endpoint to delete a user by their unique ID.",
        parameters=[
            OpenApiParameter(name='username', description="The ID of the user to delete.", required=True, type=int),
        ],
        responses={
            204: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        tags=["User"]
    )
    def destroy(self, request, pk=None):
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
