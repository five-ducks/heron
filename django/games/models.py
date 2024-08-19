from django.utils import timezone

from django.db import models
from users.models import User

class Match(models.Model):

    RESULT_CHOICES = [
        ('user_win', '사용자 승리'),  # ('저장되는 값', '사람이 읽기 쉬운 레이블')
        ('opponent_win', '상대방 승리'),
        ('pending_result', '결과 대기중'),
    ]

    TYPE_CHOICES = [
        ('tournament', '토너먼트 경기'),  # ('저장되는 값', '사람이 읽기 쉬운 레이블')
        ('match', '1대1경기'),
    ]

    user1_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='matches_as_user1')
    user2_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='matches_as_user2')
    match_result = models.CharField(max_length=40, choices=RESULT_CHOICES, blank=True, default='pending_result')
    match_start_time = models.DateTimeField(auto_now_add=True)
    match_end_time = models.DateTimeField(default=timezone.now)
    user1_grade = models.IntegerField(blank=True, default=0)
    user2_grade = models.IntegerField(blank=True, default=0)
    match_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='match')

    def __str__(self):
        return f"{self.user_id} vs {self.rival_id} is {self.match_result} at {self.match_end_time}"

class Tournament(models.Model):

    semifinal1 = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='semifinal_matches1')
    semifinal2 = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='semifinal_matches2')
    bonus_match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='bonus_matches')
    final = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='final_matches')
