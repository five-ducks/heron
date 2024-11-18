from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser


User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Django Channels 미들웨어: 쿠키에서 JWT를 읽어 사용자 인증
    """
    async def __call__(self, scope, receive, send):
        # HTTP 헤더에서 쿠키 읽기
        cookies = self.parse_cookies(scope['headers'])
        token = cookies.get('access_token')  # JWT 토큰 읽기

        # 사용자 인증
        scope['user'] = await self.get_user_from_token(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)
    # BaseMiddleware의 __call__ 메서드를 오버라이드 합니다.
    # django channels를 지원하는 middlware이므로 비동기 작업을 지원합니다.

    def parse_cookies(self, headers):
        # HTTP 헤더에서 쿠키를 파싱
        for header_name, header_value in headers:
            if header_name == b'cookie':
                cookie_values = header_value.decode()
                cookie_set = dict(item.split('=') for item in cookie_values.split('; '))
                return cookie_set
        return {}
    # b'' 의 경우 byte 문자열을 표현할때 사용합니다.
    # python은 string을 지원하지만 네트워크 통신에서는 byte 문자열로 처리를 해야 합니다.
    # headers는 tuple의 형식을 가지며, header_name: header_value 의 조합입니다.
    # cookies는 access_token=jjksjjfkdgjdfahfkds; session_id=asdfjaklsdf 와 같은 형태를 가집니다.
    # 따라서, ';' 기준으로 분할후 '=' 기준으로 다시한번 분할하여 dict 형태로 만든 cookie_set을 반환하게 됩니다.

    @sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)  # JWT 검증
            username = access_token['username']  # JWT 페이로드에서 username 추출
            user = User.objects.get(username=username)  # 데이터베이스에서 사용자 조회
            close_old_connections()  # 데이터베이스 연결 정리
            return user
        except Exception:
            return AnonymousUser()
# ws에서 jwt를 사용할 때 인증을 처리하기 위한 middleware

class CookieToAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        # 쿠키에서 access_token 가져오기
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            # Authorization 헤더처럼 설정
        return self.get_response(request)
    # django에서 연결을 처리할때 마다 호출되는 메서드
# https에서 jwt 사용시 authorize 헤더를 설정하기 위한 middleware