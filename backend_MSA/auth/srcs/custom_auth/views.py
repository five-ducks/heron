from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample
import requests

from .serializers import (
    JoinSerializer,
    LoginSerializer
)

join_api_url = "http://server-user:8001/internal/users/join/"
delete_user_api_url = "http://server-user:8001/internal/users/self/"

class AuthViewSet(viewsets.ViewSet):

    """
    A ViewSet for managing authentication.
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
                        value={ "error": "토큰 정보가 일치하지 않습니다" },
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
            # Serializer를 통해 유효성 검사
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                elif int(error_code[0]) == 409:
                    raise PermissionError(str(detail[0]))
   
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
            # AnonymousUser 인 경우 에러처리
            if request.user.is_anonymous:
                raise ValueError("이미 로그아웃 되었습니다")
            
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 로그아웃 API


##### CREATE, DELETE #####
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
    def join(self, request):
        try:
            # Serializer를 통해 유효성 검사
            serializer = JoinSerializer(data=request.data)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                
            # server-user 컨테이너에 join api 요청
            response = requests.post(
                url=join_api_url,
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    "username": serializer.validated_data['username'],
                    "profile_img": serializer.validated_data['profile_img']
                }
            )

            # 400 ~ 500대의 status code는 exception 반환
            response.raise_for_status()

            # 문제 없으면 user 생성
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 회원가입 API

    @extend_schema(
        methods=['DELETE'],
        summary="Unsubscribing",
        description="Delete user information",
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
            user = request.user

            # AnonymousUser이면 에러 처리
            if user.is_anonymous:
                raise PermissionError("로그인 상태가 아닙니다")
            
            # server-user 컨테이너에 join api 요청
            token = request.COOKIES.get('access_token')
            response = requests.delete(
                url=delete_user_api_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )

            # 400 ~ 500대의 status code는 exception 반환
            response.raise_for_status()

            # user를 바로 삭제하지 않고 is_active 필드를 false 로 변경
            user.is_active = False
            user.save()

            # cookie에서 jwt를 삭제하도록 response 설정
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            return response
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 회원탈퇴 API
