from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class OAuthLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    
    def to_internal_value(self, data):
        if 'username' not in data:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## requset의 fieldname이 잘못된 경우
        
        username = data.get('username')
        if not username:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우
        
        return super().to_internal_value(data)
    def validate(self, data):
        user = self.instance
        if user is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 username 또는 password 입니다"
                }
            )
        ## request와 일치하는 유저정보가 없는 경우
        
        if user.status != User.STATUS_MAP['오프라인']:
            raise serializers.ValidationError(
                {
                    "error_code": 409,
                    "detail": "다른 기기에서 이미 로그인되어 있습니다"
                }
            )
        ## 중복 로그인을 시도하는 경우
        
        return {'user': user}
    def save(self):
        user = self.validated_data['user']
        user.status = User.STATUS_MAP['온라인']
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)
    
    def to_internal_value(self, data):
        for fieldname in ['username', 'password']:
            if fieldname not in data:
                raise serializers.ValidationError(
                    {
                        "error_code": [400],
                        "detail": ["필드 이름이 잘못되었습니다"]
                    }
                )
        ## requset의 fieldname이 잘못된 경우
        
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우
        
        return super().to_internal_value(data)
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError(
                {
                    "error_code": 400,
                    "detail": "존재하지 않는 username 또는 password 입니다"
                }
            )
        ## request와 일치하는 유저정보가 없는 경우
        
        if user.status != User.STATUS_MAP['오프라인']:
            raise serializers.ValidationError(
                {
                    "error_code": 409,
                    "detail": "다른 기기에서 이미 로그인되어 있습니다"
                }
            )
        ## 중복 로그인을 시도하는 경우
        
        return {'user': user}
    def save(self):
        user = self.validated_data['user']
        user.status = User.STATUS_MAP['온라인']
        user.save()
        return user

class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'profile_img']
        extra_kwargs = {
            'profile_img': {'required': True}
        }
        
    
    def to_internal_value(self, data):
        for fieldname in ["username", "password", "profile_img"]:
            if fieldname not in data:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 값이 비어있습니다"]
                }
            )
        ## request의 fieldvalue가 비어있는 경우
        return super().to_internal_value(data)

    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            password = self.validated_data['password'],
            profile_img = self.validated_data['profile_img'],
        )
        user.save()
        return user
    # database에 user객체를 생성합니다.

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']
        
    def to_internal_value(self, data):
        for fieldname in data:
            if fieldname not in ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']:
                raise serializers.ValidationError(
                {
                    "error_code": [400],
                    "detail": ["필드 이름이 잘못되었습니다"]
                }
            )
        ## 잘못된 필드이름 확인
        
        return super().to_internal_value(data)
    
    def save(self):
        user = self.instance
        for fieldname, fieldvalue in self.validated_data.items():
            if fieldvalue == '':
                fieldvalue = '텍스트를 입력하세요'
            setattr(user, fieldname, fieldvalue)      
        user.save()
        return user
        
        
