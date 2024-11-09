from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
from django.contrib.auth import login, logout

from django.db.models import Q
from .models import User
from friends.models import Friend
from games.models import Match

from .serializers import (
    JoinSerializer,
    LoginSerializer,
    UpdateUserSerializer,
    CreateFriendshipSerializer,
    DeleteFriendshipSerializer,
    RetrieveFriendSerializer,
    RetrieveSearchUserSerializer,
    RetrieveSearchUserResponseSerializer,
    RetrieveUserSerializer
)

from django.views.decorators.csrf import csrf_exempt

class UserViewSet(viewsets.ViewSet):

    """
    A ViewSet for managing users.
    """

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
                        name="Fieldname Error",
                        value={ "error": "필드 이름이 잘못되었습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Fieldvalue Error",
                        value={ "error": "존재하지 않는 username 또는 password 입니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Field value is empty",
                        value={ "error": "필드 값이 비어있습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample
                    (
                        name="Session mismatch error",
                        value={ "error": "세션 정보가 일치하지 않습니다" },
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
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                elif int(error_code[0]) == 409:
                    raise PermissionError(str(detail[0]))

            user = serializer.validated_data.get('user')
            login(request, user)
            serializer.save()
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
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Fieldname Error",
                        value={ "error": "필드 이름이 잘못되었습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Fieldvalue Error",
                        value={ "error": "필드 값이 비어있습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Duplicate Username Error",
                        value={ "error": "사용중인 username 입니다" },
                        media_type='application/json'
                    )
                ]
            ),
            500: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Internal Server Error",
                examples=[
                    OpenApiExample(
                        name="Undefined Behavior",
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
            serializer = JoinSerializer(data=request.data)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
            
            serializer.save()
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
                response=RetrieveSearchUserResponseSerializer,
                description="Successfully found user"
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
            serializer = RetrieveSearchUserSerializer(instance=request.user, data=request.query_params)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                elif int(error_code[0]) == 403:
                    raise PermissionError(str(detail[0]))
                elif int(error_code[0]) == 404:
                    raise LookupError(str(detail[0]))
            
            users = serializer.validated_data['users']
            users_data = [
                {
                    "username": user.username,
                    "status_msg": user.status_msg,
                    "profile_img": user.profile_img,
                    "is_friend": Friend.objects.filter(username=request.user, friendname=user).exists()
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
    

##### CREATE, READ, DELETE #####
    @extend_schema(
        methods=['GET'],
        summary="Get the user's friend list",
        description="Return the user's friend list",
        responses={
            200: OpenApiResponse(
                response=RetrieveFriendSerializer,
                description="Successfully returned the friends list"
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
    @extend_schema(
        methods=['POST'],
        summary="Create the user's new friendship",
        description="Add new recorde to friends table",
        request=CreateFriendshipSerializer,
        responses={
            201: OpenApiResponse(description="Successfully create the user's new friendship"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Fieldname Error",
                        value={ "error": "필드 이름이 잘못되었습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Fieldvalue Error",
                        value={ "error": "필드 값이 비어있습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Not exists friendname",
                        value={ "error": "존재하지 않는 friendname입니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Not exists friendname",
                        value={ "error": "유저 본인을 친구추가 할 수 없습니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Not exists friendname",
                        value={ "error": "이미 친구상태 입니다" },
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
        parameters=[
            OpenApiParameter(
                name='friendname',
                description='Delete friendship by friendname',
                required=True,
                type=str
            ),
        ],
        methods=['DELETE'],
        summary="Delete the user's friendship",
        description="Delete record the user's friendship",
        responses={
            200: OpenApiResponse(description="Successfully deleted the users's friendship"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        name="Not already friends",
                        value={ "error": "이미 친구상태가 아닙니다" },
                        media_type='application/json'
                    ),
                    OpenApiExample(
                        name="Not exists friendname",
                        value={ "error": "존재하지 않는 friendname입니다" },
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
    @action(detail=False, methods=['get', 'post', 'delete'], url_path="self/friends")
    def manage_friends(self, request, friend_name=None):
        try:
            user = request.user
            if user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            if request.method == 'GET':    
                friends = Friend.objects.filter(username=user)
                if not friends.exists():
                    return Response(status=status.HTTP_204_NO_CONTENT)
                
                friends_data = []
                for friend in friends:
                    friend_user = friend.friendname
                    matches = Match.objects.filter((Q(match_username1=friend_user) | Q(match_username2=friend_user)) & ~Q(match_result='pending_result'))
                    friends_data.append(
                        {
                            "username": friend_user.username,
                            "status_msg": friend_user.status_msg,
                            "status": friend_user.status,
                            "exp": friend_user.exp,
                            "win_cnt": friend_user.win_cnt,
                            "lose_cnt": friend_user.lose_cnt,
                            "profile_img": friend_user.profile_img,
                            "matches": [
                                {
                                    'user1_name': match.match_username1.username,
                                    'user2_name': match.match_username2.username,
                                    'user1_profile_img': match.match_username1.profile_img,
                                    'user2_profile_img': match.match_username2.profile_img,
                                    'match_result': match.match_result,
                                    'match_start_time': match.match_start_time,
                                    'match_end_time': match.match_end_time,
                                    'user1_grade': match.username1_grade,
                                    'user2_grade': match.username2_grade,
                                    'match_type': match.match_type
                                } 
                                for match in matches.order_by('-match_end_time')[:5]
                            ]
                        }
                    )

                return Response(friends_data, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                serializer = CreateFriendshipSerializer(instance=request.user, data=request.data)
                if not serializer.is_valid():
                    error_code = serializer.errors.get('error_code')
                    detail = serializer.errors.get('detail')
                    if int(error_code[0]) == 400:
                        raise ValueError(str(detail[0]))
                
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            elif request.method == 'DELETE':
                serializer = DeleteFriendshipSerializer(instance=request.user, data=request.query_params)
                if not serializer.is_valid():
                    error_code = serializer.errors.get('error_code')
                    detail = serializer.errors.get('detail')
                    if int(error_code[0]) == 400:
                        raise ValueError(str(detail[0]))

                serializer.save()
                return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # 예기치 못한 오류가 발생한 경우
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # [GET]     user 본인의 친구목록 및 정보를 얻어오는 API
    # [POST]    user 본인의 친구관계를 추가하는 API
    # [DELETE]  user 본인의 친구관계를 삭제하는 API


##### READ, UPDATE, DELETE #####
    @extend_schema(
        methods=['GET'],
        summary="Get details about the user",
        description="Get the user's details through authentication",
        responses={
            200: OpenApiResponse(
                response=RetrieveUserSerializer,
                description="Successfully obtaining user details",
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
        request = UpdateUserSerializer,
        responses={
            200: OpenApiResponse(description="Update user details successfully"),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="Fieldname Error",
                        value={ "error": "필드 이름이 잘못되었습니다" },
                        media_type='application/json'
                    )
                ]
            ),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not Logged In",
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
                        name="Undefined Behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @extend_schema(
        methods=['DELETE'],
        summary="Unsubscribing",
        description="Delete user information",
        request = UpdateUserSerializer,
        responses={
            200: OpenApiResponse(description="Userinfo deleted successfully"),
            403: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Don't have permission to access the data",
                examples=[
                    OpenApiExample(
                        name="Not Logged In",
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
                        name="Undefined Behavior",
                        value={ "error": "시스템 에러 메세지가 출력됩니다" },
                        media_type='application/json'
                    )
                ]
            )
        },
        tags=["User"]
    )
    @action(detail=False, methods=['get', 'patch', 'delete'])
    def self(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            if request.method == 'GET':
                matches = Match.objects.filter((Q(match_username1=user) | Q(match_username2=user)) & ~Q(match_result='pending_result'))
                user_data = {
                    'username': user.username,
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
                    ],
                    'matches': [
                        {
                            'user1_name': match.match_username1.username,
                            'user2_name': match.match_username2.username,
                            'user1_profile_img': match.match_username1.profile_img,
                            'user2_profile_img': match.match_username2.profile_img,
                            'match_result': match.match_result,
                            'match_start_time': match.match_start_time,
                            'match_end_time': match.match_end_time,
                            'user1_grade': match.username1_grade,
                            'user2_grade': match.username2_grade,
                            'match_type': match.match_type
                        } 
                        for match in matches.order_by('-match_end_time')[:5]
                    ]
                }

                return Response(user_data, status=status.HTTP_200_OK)
            elif request.method == 'PATCH':
                serializer = UpdateUserSerializer(instance=request.user, data=request.data)
                if not serializer.is_valid():
                    error_code = serializer.errors.get('error_code')
                    detail = serializer.errors.get('detail')
                    if int(error_code[0]) == 400:
                        raise ValueError(str(detail[0]))
                
                serializer.save()
                return Response(status.HTTP_200_OK)
            elif request.method == 'DELETE':
                user.delete()
                return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # [GET]     user 본인의 상세정보를 얻어오는 API
    # [PATCH]   user 본인의 상세정보를 수정하는 API
    # [DELETE]  회원탈퇴를 진행하는 API
