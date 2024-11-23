from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser


# ws에서 jwt를 사용할 때 인증을 처리하기 위한 middleware
class JWTChannelAuthMiddleware(BaseMiddleware):

    """
    Django Channels 미들웨어: 쿠키에서 JWT를 읽어 사용자 인증
    """

    # 기존의 jwtAuthenticate 를 secret_key 만 검증하도록 수정했습니다.
    async def __call__(self, scope, receive, send):
        try:
            # HTTP 헤더에서 쿠키 읽기
            cookies = self.parse_cookies(scope['headers'])
            token = cookies.get('access_token')

            # 올바른 토큰인지 확인하고 문제가 있으면 exception 발생
            AccessToken(token)

            return await super().__call__(scope, receive, send)
        except Exception:
            # send 함수를 통해 웹소켓 연결 종료
            await send(
                {
                    "type": "websocket.close",
                    "code": 4003
                }
            )

    # b'' 의 경우 byte 문자열을 표현할때 사용합니다.
    # python은 string을 지원하지만 네트워크 통신에서는 byte 문자열로 처리를 해야 합니다.
    # headers는 tuple의 형식을 가지며, header_name: header_value 의 조합입니다.
    # cookies는 access_token=jjksjjfkdgjdfahfkds; session_id=asdfjaklsdf 와 같은 형태를 가집니다.
    # 따라서, ';' 기준으로 분할후 '=' 기준으로 다시한번 분할하여 dict 형태로 만든 cookie_set을 반환하게 됩니다.
    def parse_cookies(self, headers):
        # HTTP 헤더에서 쿠키를 파싱
        for header_name, header_value in headers:
            if header_name == b'cookie':
                cookie_values = header_value.decode()
                cookie_set = dict(item.split('=') for item in cookie_values.split('; '))
                return cookie_set
        return {}


# https에서 jwt 사용시 authorize 헤더를 설정하기 위한 middleware
class CookieToAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # django에서 연결을 처리할때 마다 호출되는 메서드
    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')

        if access_token:
            # Authorization 헤더 설정
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return self.get_response(request)


# htts 통신시 SECRET_KEY를 기반으로 JWT를 검증하기 위한 authenticator
class CustomJWTAuthentication(BaseAuthentication):
    
    """
    REST_FRAMEWORK에서 사용자를 인증합니다.
    """
    
    def authenticate(self, request):
        try:
            # Authorization 헤더를 가져옴
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                raise Exception("Authorization header is None")
            
            # Authorization 헤더 값 분리
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer' or token is None:
                raise Exception("Invalid token")
            
            # 유효성 검증
            AccessToken(token)

            return (AnonymousUser(), token)
        except TokenError as e:
            raise AuthenticationFailed(str(e))
        except Exception as e:
            raise AuthenticationFailed(str(e))


    def authenticate_header(self, request):
        """
        인증 실패 시 클라이언트에 보낼 WWW-Authenticate 헤더를 반환합니다.
        """
        return 'Bearer realm="api"'