from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import User
from friends.models import Friend

from .serializers import (
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
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="username 중복에러",
                        value={
                            "errors": {
                                "username": ["사용중인 username 입니다"]
                            }
                        },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            user.status = User.STATUS_MAP['온라인']
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {"errors": serializer.errors},
            # errors에 ValidationError를 통해 생성된 오류를 담아 반환합니다.
            # errors에서 필드별로 오류를 확인할 수 있습니다.
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="User login",
        description="Endpoint to log in a user and return an authentication token.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="User logged in successfully"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="username / password 입력에러",
                        value={
                            "errors": {
                                "non_field_errors": ["username 또는 password가 잘못 되었습니다."]
                            }
                        },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="중복 login 에러",
                        value={
                            "errors": {
                                "non_field_errors": ["다른 기기에서 이미 로그인되어 있습니다"]
                            }
                        },
                        media_type='application/json'
                    ),
                ]
            )
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
                user.status = User.STATUS_MAP['온라인']
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "errors" : serializer.errors
                        # 유효하지 않은 username / password인 경우
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                "errors": {
                    "non_field_errors": "다른 기기에서 이미 로그인되어 있습니다"
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="User logout",
        description="Endpoint to log out a user and invalidate the session.",
        responses={
            200: OpenApiResponse(description="User logged out successfully"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="중복 logout 에러",
                        value={
                            "errors": {
                                "non_field_errors": ["이미 로그아웃 되었습니다"]
                            }
                        },
                        media_type='application/json'
                    )
                ]
            ),
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        if request.user.is_authenticated:
            request.user.status = User.STATUS_MAP['오프라인']
            request.user.save()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                "errors": {
                    "non_field_errors": "이미 로그아웃 되었습니다"
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

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
