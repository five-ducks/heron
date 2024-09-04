from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
from django.contrib.auth import login, logout

from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import User
from friends.models import Friend

from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    UserUpdateSerializer
)

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing users.
    """
    queryset = User.objects.all()
    lookup_field = 'username'

##### 인증관련 #####
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
                        name="Input error",
                        value={ "error": "username 또는 password가 잘못 되었습니다." },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Duplicate login error",
                        value={ "error": "다른 기기에서 이미 로그인되어 있습니다" },
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
                    {"error" : "username 또는 password가 잘못 되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": "다른 기기에서 이미 로그인되어 있습니다"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # 로그인 API
    
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
                        name="Duplicate login error",
                        value={ "error": "이미 로그아웃 되었습니다" },
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
            {"errors": "이미 로그아웃 되었습니다"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # 로그아웃 API


##### CREATE #####
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
                        name="Duplicate username errors",
                        value={ "error": "사용중인 username 입니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def join(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            user.status = User.STATUS_MAP['온라인']
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {"error": "사용중인 username 입니다"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # 회원가입 API


##### READ #####
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                description='Search users by username',
                required=True,
                type=str
            ),
        ],
        summary="Search user",
        description="Find users based on search term",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successfully found user",
                examples=[
                    OpenApiExample(
                        name="User find success",
                        value={
                            "username": "string",
                            "status_msg": "string",
                            "profile_img": "int",
                            "is_friend": "bool"
                        },
                        media_type='application/json'
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="The query is empty",
                        value={ "error": "유저 이름을 입력해주세요" },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        name="User find fail",
                        value={ "error": "일치하는 유저가 없습니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    def list(self, request):
        username = request.query_params.get('search', '')
        if username:
            users = User.objects.filter(username__icontains=username).exclude(username=request.user.username)
            if users:
                users_data = []
                for user in users:
                    is_friend = Friend.objects.filter(user1_id=request.user, user2_id=user)
                    users_data.append({
                        "username": user.username,
                        "status_msg": user.status_msg,
                        "profile_img": user.profile_img,
                        "is_friend": is_friend.exists()
                    })
                return Response(
                    users_data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "일치하는 유저가 없습니다"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "유저 이름을 입력해주세요"},
                status=status.HTTP_404_NOT_FOUND
            )
    # 특정 keyword를 기반으로 user를 찾는 API
    
    @extend_schema(
        summary="Get the user's friend list",
        description="Return the user's friend list",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successfully returned the friends list",
                examples=[
                    OpenApiExample(
                        name="Friendlist",
                        value={
                            "username": "string",
                            "status_msg": "string",
                            "status": "int",
                            "profile_img": "int"
                        },
                        media_type='application/json'
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        name="Friendlist is empty",
                        value={ "error": "친구목록이 비어있습니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get'], url_path="self/friends")
    def retrieve_friendlist(self, request):
        user = request.user
        if user.is_authenticated:
            friends = Friend.objects.filter(user1_id=user)
            if friends.exists():
                friends_data = []
                for friend in friends:
                    friends_data.append({
                        "username": friend.user2_id.username,
                        "status_msg": friend.user2_id.status_msg,
                        "status": friend.user2_id.status,
                        "profile_img": friend.user2_id.profile_img
                    })
                return Response(
                    friends_data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "친구목록이 비어있습니다"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "로그인 상태가 아닙니다"},
                status=status.HTTP_400_BAD_REQUEST
            )
    # user 본인의 친구목록을 찾는 API


##### READ, UPDATE #####
    @extend_schema(
        methods=['GET'],
        summary="Get details about the user",
        description="Get the user's details through authentication",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successfully obtaining user details",
                examples=[
                    OpenApiExample(
                        name="userinfo details",
                        value={
                            'exp': 'int',
                            'profile_img': 'int',
                            'win_cnt': 'int',
                            'lose_cnt': 'int',
                            'status_msg': 'string',
                            'macrotext': [
                                'string',
                                'string',
                                'string',
                                'string',
                                'string'
                            ]
                        },
                        media_type='application/json'
                    )
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @extend_schema(
        methods=['PATCH'],
        summary="Update user details",
        description="Update user details through authentication",
        request = UserUpdateSerializer,
        responses={
            200: OpenApiResponse(),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get', 'patch'])
    def self(self, request):
        user = request.user
        if request.method == 'GET':
            if user.is_authenticated:
                return Response(
                    {
                        'exp': user.exp,
                        'profile_img': user.profile_img,
                        'win_cnt': user.win_cnt,
                        'lose_cnt': user.lose_cnt,
                        'status_msg': user.status_msg,
                        'macrotext': [
                            user.macrotext1,
                            user.macrotext2,
                            user.macrotext3,
                            user.macrotext4,
                            user.macrotext5
                        ]
                    },
                    status.HTTP_200_OK
                )
            return Response(
                {"errors": "로그인 상태가 아닙니다"},
                status.HTTP_404_NOT_FOUND
            )
        elif request.method == 'PATCH':
            if user.is_authenticated:
                for fieldname in request.data:
                    setattr(user, fieldname, request.data.get(fieldname))
                return Response(status.HTTP_200_OK)
            return Response(
                {"error": "로그인 상태가 아닙니다"},
                status=status.HTTP_400_BAD_REQUEST
            )
    # [GET]    user 본인의 상세정보를 얻어오는 API
    # [PATCH]  user 본인의 상세정보를 수정하는 API