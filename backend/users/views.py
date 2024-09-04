from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import User
from friends.models import Friend

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    ProfileUpdateSerializer,
    LoginSerializer,
    FriendListSerializer
)

def get_online_status(user_id):
    return True
    # Example logic: Replace this with your actual logic
    # This might be a Redis call, a lookup in a cache, or any other service
    online_users = get_online_users_from_cache()  # Placeholder function
    return online_users.get(user_id, False)  # Return True if online, otherwise False

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing users.
    """
    def get_queryset(self):
        return User.objects.all()

    @extend_schema(
        summary="Create a new user",
        description="Endpoint to create a new user in the system.",
        request=SignUpSerializer,
        responses={
            201: OpenApiResponse(description="User created successfully"),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            profile_image = serializer.validated_data["profile_img"]
            if User.objects.filter(username=username).exists():
                serializer.add_error("username", "입력한 사용자명은 이미 사용중입니다")
            if serializer.errors:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    profile_img=profile_image,
                )
                login(request, user)
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get a user by ID",
        description="Endpoint to retrieve a user by their unique ID.",
        responses={
            200: OpenApiResponse(description="User retrieved successfully"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["User"]
    )
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update a user by ID",
        description="Endpoint to update a user's information by their unique ID.",
        request=ProfileUpdateSerializer,
        responses={
            200: OpenApiResponse(description="User updated successfully"),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["User"]
    )
    def update(self, request, pk=None):
        # TODO: Need to check whether if the user is updating their own profile
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a user by ID",
        description="Endpoint to delete a user by their unique ID.",
        responses={
            204: OpenApiResponse(description="User deleted successfully"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["User"]
    )
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="User login",
        description="Endpoint to log in a user and return an authentication token.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="User logged in successfully"),
            400: OpenApiResponse(description="Bad request"),
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        if request.user.is_anonymous:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="User logout",
        description="Endpoint to log out a user and invalidate the session.",
        responses={
            200: OpenApiResponse(description="User logged out successfully"),
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve all friends for a specific user",
        description="Retrieve all friends associated with a specific user ID.",
        responses={
            200: FriendListSerializer(many=True),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["User"]
    )
    @action(detail=True, methods=['get'])
    def friends(self, request, pk=None):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)

        # Step 1: Fetch the friend relationships
        friends = Friend.objects.filter((Q(user1_id=user) | Q(user2_id=user)) & Q(status="accepted"))
        if not friends.exists():
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Get the online status for each friend
        friends_data = []
        for friend in friends:
            if friend.user1_id == user:
                friend_user = friend.user2_id
            else:
                friend_user = friend.user1_id

            friend_status = get_online_status(friend_user.id)  # Assuming this method exists

            # Prepare data for serialization
            friends_data.append({
                'friend_nickname': friend_user.nickname,
                'friend_status': friend_status,  # Online status from the external service
                'friend_profile_image_url': friend_user.profile_img if friend_user.profile_img else None
            })

        # Serialize the data
        serializer = FriendListSerializer(friends_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
