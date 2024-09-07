from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
from django.shortcuts import redirect
from django.conf import settings
import requests

from users.serializers import (
    SignUpSerializer,
    # OAuthLoginSerializer,
    UserUpdateSerializer
)

class OAuthViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling OAuth login via 42 API.
    """
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    redirect_uri = "http://localhost:8000/oauth/login/redirect"

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
            f"?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"
        )
        return redirect(url)

    @action(detail=False, methods=['get'], url_path="login/redirect")
    def login_redirect(self, request):
        # 42 API에서 받은 code로 토큰 교환
        code = request.GET.get("code")
        token = self.exchange_code_for_token(code)
        user = self.get_42user_info(token)

        # 42 API에서 받은 username으로 유저가 이미 있는지 확인
        username = user.get("login")
        # user = User.objects.filter(username=username).first()

        return Response({"user": user}, status=status.HTTP_200_OK)

    def exchange_code_for_token(self, code):
        # 토큰 교환을 위한 요청 로직
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
        response_data = response.json()
        return response_data.get("access_token")

    def get_42user_info(self, token):
        # 42 API를 사용해 사용자 정보 요청
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://api.intra.42.fr/v2/me", headers=headers)
        return response.json()
