from rest_framework import serializers
from .models import Match, Tournament

class MatchCreationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['user2_id', 'match_result', 'match_start_time', 'match_end_time', 'user1_grade', 'user2_grade', 'match_type']


class MatchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'user1_id', 'user2_id', 'match_result', 'match_start_time', 'match_end_time', 'user1_grade', 'user2_grade', 'match_type']


class TournamentCreationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['semifinal1', 'semifinal2', 'bonus_match', 'final']


class TournamentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'semifinal1', 'semifinal2', 'bonus_match', 'final']

class TournamentRankingResponseSerializer(serializers.Serializer):
    rank = serializers.IntegerField(help_text="User's rank in the tournament.")
    user_id = serializers.IntegerField(help_text="Unique identifier for the user.")
    user_nickname = serializers.CharField(help_text="Nickname of the user.")
    score = serializers.IntegerField(help_text="Score achieved by the user in the tournament.")