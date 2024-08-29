from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'profile_img']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'profile_img', 'exp', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']

    # Override some fields to be optional for profile updates
    nickname = serializers.CharField(required=False)
    profile_img = serializers.IntegerField(required=False)
    exp = serializers.IntegerField(required=False)

class RetrieveSerializer(serializers.ModelSerializer):
    # TODO: Implement this serializer
    # class Meta:
    #     model = User
    #     fields =
    pass

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username used as the login ID for the user.")
    password = serializers.CharField(help_text="Password for the user login.")

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("User not found.")
        return {'user': user}

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'profile_img']

class FriendListSerializer(serializers.Serializer):
    friend_nickname = serializers.CharField(read_only=True, help_text="Friend's nickname")
    friend_status = serializers.BooleanField(read_only=True, help_text="Friend's online status")
    friend_profile_image_url = serializers.IntegerField(read_only=True, help_text="Friend's profile image id")