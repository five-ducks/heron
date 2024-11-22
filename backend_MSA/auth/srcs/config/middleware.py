# https에서 jwt 사용시 authorize 헤더를 설정하기 위한 middleware
class CookieToAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # django에서 연결을 처리할때 마다 호출되는 메서드
    def __call__(self, request):
        # 쿠키에서 access_token 가져오기
        access_token = request.COOKIES.get('access_token')

        # access_token이 존재하는 경우 Authorization 헤더 설정
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        return self.get_response(request)