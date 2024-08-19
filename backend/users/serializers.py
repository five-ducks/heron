from rest_framework import serializers
from .models import User

class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token required for logout.")


class CreateUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'profile_img']


class UserResponseSerializer(serializers.ModelSerializer):
    macrotexts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_img', 'macrotexts']

    def get_macrotexts(self, obj):
        return {
            'macrotext1': obj.macrotext1,
            'macrotext2': obj.macrotext2,
            'macrotext3': obj.macrotext3,
            'macrotext4': obj.macrotext4,
            'macrotext5': obj.macrotext5,
        }


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="The user name for login")
    password = serializers.CharField(write_only=True, help_text="The password for login in clear text")


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token returned upon successful login.")
    expires_at = serializers.DateTimeField(help_text="Expiration time of the authentication token.")
