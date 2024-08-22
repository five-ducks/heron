from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['username', 'password', 'exp']

    # Override some fields to be optional for profile updates
    nickname = serializers.CharField(required=False)
    profile_img = serializers.IntegerField(required=False)

#---------------------------------------------------
# The following serializers are for the API documentation
class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token required for logout.")

class CreateUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'profile_img']

class UpdateUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['exp']
    # nickname = serializers.CharField(required=False, help_text="Nickname for the user.")
    # profile_img = serializers.IntegerField(required=False, help_text="Profile image ID for the user, selectable from predefined options.")
    # macrotext1 = serializers.CharField(required=False, help_text="Macro text 1, default is 'good game'.")
    # macrotext2 = serializers.CharField(required=False, help_text="Macro text 2, default is 'thanks'.")
    # macrotext3 = serializers.CharField(required=False, help_text="Macro text 3, default is 'bye bye'.")
    # macrotext4 = serializers.CharField(required=False, help_text="Macro text 4, default is 'goooooood!'.")
    # macrotext5 = serializers.CharField(required=False, help_text="Macro text 5, default is 'hello'.")

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="The user name for login")
    password = serializers.CharField(write_only=True, help_text="The password for login in clear text")

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token returned upon successful login.")
    expires_at = serializers.DateTimeField(help_text="Expiration time of the authentication token.")

class FriendListSerializer(serializers.Serializer):
    friend_nickname = serializers.CharField(read_only=True, help_text="Friend's nickname")
    friend_status = serializers.BooleanField(read_only=True, help_text="Friend's online status")
    friend_profile_image_url = serializers.IntegerField(read_only=True, help_text="Friend's profile image id")