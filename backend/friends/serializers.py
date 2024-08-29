from rest_framework import serializers
from .models import Friend

class FriendCreationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['user2_id', 'status']

class FriendResponseSerializer(serializers.ModelSerializer):
    friend_nickname = serializers.CharField(source='user2_id.nickname', read_only=True)
    friend_status = serializers.SerializerMethodField()
    friend_profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['user1_id', 'user2_id', 'status', 'friend_nickname', 'friend_status', 'friend_profile_image_url']

    def get_friend_status(self, obj):
        # Assuming you have a way to check if the friend is online or offline.
        # This is just a placeholder example:
        return "online" if obj.user2_id.is_online else "offline"

    def get_friend_profile_image_url(self, obj):
        # Assuming you have a function or property to get the profile image URL
        # This is just a placeholder example:
        return obj.user2_id.get_profile_image_url()