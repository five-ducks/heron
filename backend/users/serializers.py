from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            profile_img=validated_data['profile_img']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'profile_img', 'email', 'first_name', 'last_name', 'macrotext1', 'macrotext2', 'macrotext3', 'macrotext4', 'macrotext5']

    # Override some fields to be optional for profile updates
    nickname = serializers.CharField(required=False)
    profile_img = serializers.IntegerField(required=False)

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username used as the login ID for the user.")
    password = serializers.CharField(help_text="Password for the user login.")

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("User not found.")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid password.")
        return data

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token returned upon successful login.")
    expires_at = serializers.DateTimeField(help_text="Expiration time of the authentication token.")

#---------------------------------------------------
# The following serializers are for the API documentation
class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token required for logout.")

class CreateUserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'profile_img']

class FriendListSerializer(serializers.Serializer):
    friend_nickname = serializers.CharField(read_only=True, help_text="Friend's nickname")
    friend_status = serializers.BooleanField(read_only=True, help_text="Friend's online status")
    friend_profile_image_url = serializers.IntegerField(read_only=True, help_text="Friend's profile image id")