from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

## serializers.ValidationError로 설정한 fieldname과 fieldvalue는 serializer.errors.get(fieldname)으로 외부에서 확인할 수 있습니다.
## 하지만 serializer.errors.get(key)을 통해 반환된 fieldvalue는 errordetail객체로 반환됩니다.
## errordetail객체는 내가 설정한 value 외의 추가적인 필드를 생성하여 담고 있습니다.
## 따라서 내가 설정한 fieldvalue를 사용하고 싶다면 int 또는 str로 변환해서 사용하면 됩니다.

##### ValidationError의 차이 #####
## to_internal_value의 경우 dict의 fieldvalue를 errordetail객체로 감싸게 됩니다.
## validate의 경우 fieldvalue를 errordetail객체로 감싸고 list로 한번 더 감싸게 됩니다.

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
        ## to_internal_value를 오버라이딩 하여 커스첨 validation check를 진행합니다.
        ## 이후 부모 클래스의 to_internal_value를 호출합니다.
    ## to_internal_value는 is_valid()를 진행할 때 validate()가 호출되기 전 호출되는 함수입니다.
    ## 해당 함수를 오버라이딩 하여 required한 username, password의 valid check를 커스텀 할 수 있습니다.
        
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
        
        
