from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from custom_auth.models import Auth
from django_otp.plugins.otp_totp.models import TOTPDevice
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample, OpenApiParameter
import qrcode
import io
import base64
from rest_framework_simplejwt.tokens import AccessToken

class TwoFAViewSet(viewsets.ViewSet):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='username',
                description='Search users by username',
                required=True,
                type=str
            ),
        ],
        summary="Generate OTP for 2FA",
        description="Generate OTP for 2FA by username",
        responses={
            200: OpenApiResponse(
                description="Success"
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
    @action(detail=False, methods=['get'])
    def generate(self, request):
        try:
            username = request.query_params.get('username')
            user = Auth.objects.filter(username=username, is_active=True).first()
            device, created = TOTPDevice.objects.get_or_create(user=user, name="default")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(device.config_url)
            qr.make(fit=True)

            # 이미지를 메모리 버퍼로 저장
            img = qr.make_image(fill="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)  # 버퍼의 시작 위치로 이동

            # Base64 인코딩
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # JSON 응답
            return Response({"qr_code": img_base64}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'])
    def verify(self, request):
        try:
            username = request.query_params.get('username')
            user = Auth.objects.filter(username=username, is_active=True).first()
            device = TOTPDevice.objects.filter(user=user, name="default").first()

            # TOTP 테이블에 생성된 device가 없거나 인증코드가 유효하지 않으면 에러
            if not device or not device.verify_token(request.data.get('code')):
                raise Exception("OTP autheticate failed")
            
            # user객체로 AccessToken 발급
            access_token = str(AccessToken.for_user(user))

            # Response에 cookie로 jwt 저장
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
            )
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
