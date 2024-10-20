from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.conf import settings
import requests

from users.models import User
from users.serializers import (
    JoinSerializer,
    LoginSerializer,
)

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
redirect_uri = "http://localhost:8000/oauth/login/redirect"


def login_redirect(request):
    # 42 API에서 받은 code로 토큰 교환
    code = request.GET.get("code")
    token = exchange_code_for_token(code)
    user = get_42user_info(token)

    # 42 API에서 받은 username으로 유저가 이미 있는지 확인
    username = user.get("login")
    user = User.objects.filter(username=username).first()
    if not user:
        try:
            # 유저가 없다면 회원가입
            new_user_data = {"username": username, "password": "42oauth", "profile_img": 1}
            serializer = JoinSerializer(data=new_user_data)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
            serializer.save()
            return JsonResponse({"detail": "user created"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        try:
            # 유저가 있다면 로그인
            user_data = {"username": username, "password": "42oauth"}
            serializer = LoginSerializer(data=user_data)
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

            return JsonResponse({"detail": "user logged in"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def exchange_code_for_token(code):
    # 토큰 교환을 위한 요청 로직
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }
    response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
    response_data = response.json()
    return response_data.get("access_token")


def get_42user_info(token):
    # 42 API를 사용해 사용자 정보 요청
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.intra.42.fr/v2/me", headers=headers)
    return response.json()


class OAuthViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling OAuth login via 42 API.
    """

    @extend_schema(
        summary="42 OAuth login",
        description="Redirects to 42 OAuth login page.",
        # request=OAuthLoginSerializer,
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
        tags=["OAuth"]
    )
    @action(detail=False, methods=['get'])
    def login(self, request):
        # OAuth 42 로그인 페이지로 리다이렉트
        url = (
            f"https://api.intra.42.fr/oauth/authorize"
            f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        return redirect(url)
