from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect
import requests

from custom_auth.models import Auth
from custom_auth.serializers import (
    JoinSerializer,
    LoginSerializer,
)

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET

redirect_uri = "http://10.18.204.91:8002/oauth/login/redirect"
join_api_url = "http://backend-user:8001/internal/users/join/"


def login_redirect(request):
    try:
        # 42 API에서 받은 code로 토큰 교환 및 user 정보 얻음
        token = exchange_code_for_token(request.GET.get("code"))
        user = get_42user_info(token)
        username = user.get("login")

        # Auth 테이블에 유저가 있는 경우 로그인
        if Auth.objects.filter(username=username, is_active=True).exists():
            user_data = {"username": username, "password": "42oauth"}

            # Serializer를 통해 유효성 검증을 하고 문제가 있으면 raise
            serializer = LoginSerializer(data=user_data, context={'request': request})
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))
                elif int(error_code[0]) == 409:
                    raise PermissionError(str(detail[0]))

            return HttpResponseRedirect(f"https://10.18.204.91/#/login/2fa?username={username}")
        # Auth 테이블에 유저가 없는 경우 회원가입
        else:
            new_user_data = {"username": username, "password": "42oauth", "profile_img": 1}
            
            # Serializer를 통해 유효성 검증을 하고 문제가 있으면 raise
            serializer = JoinSerializer(data=new_user_data)
            if not serializer.is_valid():
                error_code = serializer.errors.get('error_code')
                detail = serializer.errors.get('detail')
                if int(error_code[0]) == 400:
                    raise ValueError(str(detail[0]))

            # backend-user 컨테이너에 join api 요청
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

            # 유효성 검사에서 통과하면 회원가입            
            serializer.save()
            return HttpResponseRedirect("https://10.18.204.91")
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
            f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")
        return JsonResponse({"redirect_url": url})
