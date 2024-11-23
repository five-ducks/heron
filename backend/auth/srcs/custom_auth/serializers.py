from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Auth
import requests

get_status_api_url = "http://backend-user:8001/internal/users/status/"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def to_internal_value(self, data):
        # requset의 fieldname이 잘못된 경우
        for fieldname in ['username', 'password']:
            if fieldname not in data:
                raise serializers.ValidationError(
                    {
                        "error_code": [400],
                        "detail": ["필드 이름이 잘못되었습니다"]
                    }
                )

        # request의 fieldvalue가 비어있는 경우
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )

        return super().to_internal_value(data)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        # request와 일치하는 유저정보가 없는 경우
        if user is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 username 또는 password 입니다"
                }
            )
        
        # 이미 로그인된 상태에서 다른 유저로 로그인 시도하는 경우
        request = self.context['request']
        if request.user.is_authenticated:
            if request.user.username != user.username:
                raise serializers.ValidationError(
                    {
                        "error_code": 400,
                        "detail": "토큰 정보가 일치하지 않습니다"
                    }
                )

        # user 컨테이너에 status를 받아오기 위한 api 요청
        response = requests.get(
            url=get_status_api_url,
            headers={
                "Content-Type": "application/json",
            },
            json={
                "username": user.username
            }
        )

        # 400 ~ 500대의 status code는 exception 반환
        response.raise_for_status()

        # 중복 로그인을 시도하는 경우
        if response.json().get('status') == 1:
            raise serializers.ValidationError(
                {
                    "error_code": 409,
                    "detail": "다른 기기에서 이미 로그인되어 있습니다"
                }
            )

        return {'user': user}

class JoinSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)
    profile_img = serializers.IntegerField(required=True)

    def to_internal_value(self, data):
        # 잘못된 필드이름 확인
        for fieldname in ["username", "password", "profile_img"]:
            if fieldname not in data:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )

        # request의 fieldvalue가 비어있는 경우
        username = data.get('username')
        password = data.get('password')
        profile_img = data.get('profile_img')
        if not username or not password or not profile_img:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )

        # 중복된 유저이름 확인
        if Auth.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["사용할 수 없는 username 입니다"]
                }
            )
        return super().to_internal_value(data)

    def save(self):
        user = Auth.objects.create_user(
            username = self.validated_data['username'],
            password = self.validated_data['password'],
            is_active = True
        )
        user.save()
        return user
    # database에 user객체를 생성합니다.
