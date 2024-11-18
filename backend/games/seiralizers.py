from rest_framework import serializers
from .models import Match

class RetrieveMatchDataSerializer(serializers.Serializer):
    class Meta:
        model = Match
        fields = ['match_username1', 'match_username2', 'match_result', 'match_start_time', 'match_end_time', 'user1_grade', 'user2_grade', 'match_type']