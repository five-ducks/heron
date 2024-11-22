from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
# from rest_framework.permissions import AllowAny
from .models import User
from friends.models import Friend

from .serializers import (
    JoinSerializer,
    UpdateUserSerializer,
    CreateFriendshipSerializer,
    DeleteFriendshipSerializer,
    RetrieveFriendSerializer,
    RetrieveSearchUserSerializer,
    RetrieveSearchUserResponseSerializer,
    RetrieveUserSerializer
)

def get_user_from_token(token):
        access_token = AccessToken(token)
        username = access_token['username']
        user = User.objects.get(username=username)
        return user

class ExternalUserViewSet(viewsets.ViewSet):

    """
    A External ViewSet for managing users.
    """

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
            user = get_user_from_token(request.COOKIES.get('access_token'))
            serializer = RetrieveSearchUserSerializer(instance=user, data=request.query_params)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                elif int(error_code[0]) == 403:
                    raise PermissionError(str(detail[0]))
                elif int(error_code[0]) == 204:
                    return Response([], status=status.HTTP_200_OK)
            
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
            user = get_user_from_token(request.COOKIES.get('access_token'))
            if user.status == User.STATUS_MAP['오프라인']:
                raise PermissionError("로그인 상태가 아닙니다")
            
            if request.method == 'GET':
                friends = Friend.objects.filter(username=user)
                if not friends.exists():
                    return Response([], status=status.HTTP_200_OK)
                
                friends_data = []
                for friend in friends:
                    friend_user = friend.friendname
                    friends_data.append(
                        {
                            "username": friend_user.username,
                            "status_msg": friend_user.status_msg,
                            "status": friend_user.status,
                            "exp": friend_user.exp,
                            "win_cnt": friend_user.win_cnt,
                            "lose_cnt": friend_user.lose_cnt,
                            "profile_img": friend_user.profile_img
                        }
                    )

                return Response(friends_data, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                serializer = CreateFriendshipSerializer(instance=user, data=request.data)
                if not serializer.is_valid():
                    error_code = serializer.errors.get('error_code')
                    detail = serializer.errors.get('detail')
                    if int(error_code[0]) == 400:
                        raise ValueError(str(detail[0]))
                
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            elif request.method == 'DELETE':
                serializer = DeleteFriendshipSerializer(instance=user, data=request.query_params)
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
    @action(detail=False, methods=['get', 'patch'])
    def self(self, request):
        try:
            user = get_user_from_token(request.COOKIES.get('access_token'))
            if user.status == User.STATUS_MAP['오프라인']:
                raise PermissionError("로그인 상태가 아닙니다")
            
            if request.method == 'GET':
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
                    ]
                }

                return Response(user_data, status=status.HTTP_200_OK)
            elif request.method == 'PATCH':
                serializer = UpdateUserSerializer(instance=user, data=request.data)
                if not serializer.is_valid():
                    error_code = serializer.errors.get('error_code')
                    detail = serializer.errors.get('detail')
                    if int(error_code[0]) == 400:
                        raise ValueError(str(detail[0]))
                
                serializer.save()
                return Response(status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # [GET]     user 본인의 상세정보를 얻어오는 API
    # [PATCH]   user 본인의 상세정보를 수정하는 API

class InternalUserViewSet(viewsets.ViewSet):
    
    """
    A Internal ViewSet for managing users.
    """

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
    @action(detail=False, authentication_classes = [], methods=['post'])
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
    # 유저생성 API

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
    @action(detail=False, methods=['delete'])
    def self(self, request):
        try:
            request.user.delete()
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 유저삭제 API

    @extend_schema(
        methods=['GET'],
        summary="get status",
        description="get real time user status",
        responses={
            200: OpenApiResponse(description="Successfully get user status"),
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
    @action(detail=False, authentication_classes = [], methods=['get'])
    def status(self, request):
        try:
            user = User.objects.filter(username=request.data.get('username')).first()
            data = {
                "status": user.status
            }
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 유저삭제 API