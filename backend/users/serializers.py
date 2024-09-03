from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

# class ProfileUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['nickname', 'profile_img', 'exp', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']

#     # Override some fields to be optional for profile updates
#     profile_img = serializers.IntegerField(required=False)
#     exp = serializers.IntegerField(required=False)
## 필요없으면 주석처리된 내역 삭제 필요

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

# class FriendListSerializer(serializers.Serializer):
#     friend_username = serializers.CharField(read_only=True, help_text="Friend's username")
#     friend_status = serializers.BooleanField(read_only=True, help_text="Friend's online status")
#     friend_profile_image_id = serializers.IntegerField(read_only=True, help_text="Friend's profile image id")
## 필요없으면 주석처리된 내역 삭제 필요