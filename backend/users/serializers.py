from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username used as the login ID for the user.")
    password = serializers.CharField(help_text="Password for the user login.")

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("username 또는 password가 잘못 되었습니다.")
        return {'user': user}

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'profile_img']
    
    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            password = self.validated_data['password'],
            profile_img = self.validated_data['profile_img'],
        )
        return user
    # database에 user객체를 생성합니다.

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['status_msg', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']
