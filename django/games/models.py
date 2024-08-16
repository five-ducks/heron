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

    match_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    rival_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rival_id')
    match_result = models.CharField(max_length=40, choices=RESULT_CHOICES, blank=True, default='pending_result')
    match_start_time = models.DateTimeField(auto_now_add=True)
    match_end_time = models.DateTimeField(default=timezone.now)
    match_user_grade = models.IntegerField(blank=True, default=0)
    match_rival_grade = models.IntegerField(blank=True, default=0)
    match_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='match')

    def __str__(self):
        return f"{self.user_id} vs {self.rival_id} is {self.match_result} at {self.match_end_time}"

class Tournament(models.Model):

    tournament_id = models.AutoField(primary_key=True)
    semifinal_id1 = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='semifinal_id1')
    semifinal_id2 = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='semifinal_id2')
    bonus_match_id = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='bonus_match_id')
    final_id = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='final_id')
