from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.exceptions import ValidationError
from .serializers import LoginSerializer


class LoginSerializerTest(TestCase):

    def setUp(self):
        # 커스텀 User 모델 사용
        self.User = get_user_model()

        # 테스트용 유저 생성
        self.user = self.User.objects.create_user(
            username='testuser', password='testpass')
        self.user.status = self.User.STATUS_MAP['오프라인']
        self.user.save()

        # RequestFactory 사용하여 공통 request 객체 생성
        self.factory = RequestFactory()

    def _force_authenticate_session(self, request):
        """세션을 수동으로 추가하는 헬퍼 메서드"""
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        request.session.save()

    def _login_post_request(self, data):
        """POST 요청을 보내는 헬퍼 메서드"""
        request = self.factory.post('/login/')
        self._force_authenticate_session(request)
        return LoginSerializer(data=data, context={'request': request})

    def assertUserStatus(self, user, expected_status):
        """유저의 상태가 기대된 값과 일치하는지 확인하는 헬퍼 메서드"""
        self.assertEqual(user.status, self.User.STATUS_MAP[expected_status])

    def test_successful_login(self):
        """정상적인 로그인 테스트"""
        data = {'username': 'testuser',
                'password': 'testpass', 'force_login': False}
        serializer = self._login_post_request(data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # 유저가 온라인 상태로 변경되었는지 확인
        self.assertUserStatus(user, '온라인')

    def test_already_logged_in_without_force_login(self):
        """이미 로그인된 상태에서 force_login 없이 로그인 시도 테스트"""
        self.user.status = self.User.STATUS_MAP['온라인']
        self.user.save()

        data = {'username': 'testuser',
                'password': 'testpass', 'force_login': False}
        serializer = self._login_post_request(data)

        # 유효성 검사에서 ValidationError가 발생해야 함
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        # ValidationError에 담긴 메시지를 확인
        self.assertEqual(
            str(cm.exception.detail['detail'][0]), "다른 기기에서 이미 로그인되어 있습니다")

    def test_force_login(self):
        """이미 로그인된 상태에서 force_login=True로 강제 로그아웃 후 로그인 테스트"""
        self.user.status = self.User.STATUS_MAP['온라인']
        self.user.save()

        data = {'username': 'testuser',
                'password': 'testpass', 'force_login': True}
        serializer = self._login_post_request(data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # 강제 로그아웃 후 새로 로그인하였는지 확인
        self.assertUserStatus(user, '온라인')

    def test_invalid_password(self):
        """잘못된 비밀번호로 로그인 시도 시 ValidationError 발생"""
        data = {'username': 'testuser',
                'password': 'wrongpass', 'force_login': False}
        serializer = self._login_post_request(data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_force_login_value(self):
        """force_login 값이 올바르지 않은 경우 테스트"""
        data = {'username': 'testuser', 'password': 'testpass',
                'force_login': 'invalid_value'}
        serializer = self._login_post_request(data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
