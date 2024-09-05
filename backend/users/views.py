from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
from django.contrib.auth import login, logout

from .models import User
from friends.models import Friend

from .serializers import (
    JoinSerializer,
    LoginSerializer,
    UserUpdateSerializer
)

from django.views.decorators.csrf import csrf_exempt

class UserViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing users.
    """
    # queryset = User.objects.all()
    # lookup_field = 'username'
    ## 추후에 사용되지 않으면 삭제가 필요합니다.

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
                    )
                ]
            ),
            409: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Conflict",
                examples=[
                    OpenApiExample(
                        name="Duplicate login error",
                        value={ "error": "다른 기기에서 이미 로그인되어 있습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            if request.user.username == request.data.get("username"):
                raise PermissionError("다른 기기에서 이미 로그인되어 있습니다")
            
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                raise ValueError("username 또는 password가 잘못 되었습니다")
            
            user = serializer.validated_data['user']
            login(request, user)
            user.status = User.STATUS_MAP['온라인']
            user.save()
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                        name="Duplicate logout error",
                        value={ "error": "이미 로그아웃 되었습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            if request.user.is_anonymous:
                raise ValueError("이미 로그아웃 되었습니다")
            
            request.user.status = User.STATUS_MAP['오프라인']
            request.user.save()
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 로그아웃 API


##### CREATE #####
    @extend_schema(
        summary="Create a new user",
        description="Endpoint to create a new user in the system.",
        request=JoinSerializer,
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
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def join(self, request):
        try:
            serializer = SignUpSerializer(data=request.data)
            if not serializer.is_valid():
                raise ValueError("사용중인 username 입니다")
            
            user = serializer.save()
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
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
                        name="User find fail",
                        value={ "error": "일치하는 유저가 없습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    def list(self, request):
        try:
            if request.user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            username = request.query_params.get('search', '')
            if not username:
                raise ValueError("유저 이름을 입력해주세요")
            
            users = User.objects.filter(username__icontains=username).exclude(username=request.user.username)
            if not users:
                raise LookupError("일치하는 유저가 없습니다")
            
            users_data = [
                {
                    "username": user.username,
                    "status_msg": user.status_msg,
                    "profile_img": user.profile_img,
                    "is_friend": Friend.objects.filter(user1_id=request.user, user2_id=user).exists()
                }
                for user in users
            ]
            return Response(users_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            204: OpenApiResponse(description="friend list is empty"),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get'], url_path="self/friends")
    def retrieve_friendlist(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            friends = Friend.objects.filter(user1_id=user)
            if not friends.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            friends_data = [
                {
                    "username": friend.user2_id.username,
                    "status_msg": friend.user2_id.status_msg,
                    "status": friend.user2_id.status,
                    "profile_img": friend.user2_id.profile_img    
                }
                for friend in friends
            ]
            return Response(friends_data, status=status.HTTP_200_OK)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # 예기치 못한 오류가 발생한 경우
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
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
            200: OpenApiResponse(description="Update user details successfully"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="Invalid fieldname",
                        value={ "error": "유효하지 않은 fieldname 입니다" },
                        media_type='application/json'
                    )
                ]
            ),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not logged in",
                        value={ "error": "로그인 상태가 아닙니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal server error",
                examples=[
                    OpenApiExample(
                        name="undefined behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get', 'patch'])
    def self(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            if request.method == 'GET':
                user_data = {
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
                }
                return Response(user_data, status=status.HTTP_200_OK)
            elif request.method == 'PATCH':
                for fieldname, value in request.data.items():
                    if hasattr(user, fieldname):
                        if value == '':
                            value = '텍스트를 입력하세요'
                        setattr(user, fieldname, value)
                    else:
                        raise ValueError(f"유효하지 않은 '{fieldname}' 입니다")
                user.save()
                return Response(status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # [GET]    user 본인의 상세정보를 얻어오는 API
    # [PATCH]  user 본인의 상세정보를 수정하는 API
