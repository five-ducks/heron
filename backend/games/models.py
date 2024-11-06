from django.utils import timezone

from django.db import models
from users.models import User

class Match(models.Model):

    RESULT_CHOICES = [
        ('user1_win', '유저1 승리'),
        ('user2_win', '유저2 승리'),
        ('pending_result', '결과 대기중'),
    ]

    TYPE_CHOICES = [
        ('tournament', '토너먼트 경기'),
        ('single', '1대1경기'),
    ]

    match_username1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='matches_as_user1',
        help_text="Reference to the first user participating in the match."
    )
    match_username2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='matches_as_user2',
        help_text="Reference to the second user participating in the match."
    )
    match_result = models.CharField(
        max_length=40,
        choices=RESULT_CHOICES,
        blank=True,
        default='pending_result',
        help_text="Result of the match."
    )
    match_start_time = models.DateTimeField(
        auto_now_add=True,
        help_text="Start time of the match."
    )
    match_end_time = models.DateTimeField(
        default=timezone.now,
        help_text="End time of the match."
    )
    username1_grade = models.IntegerField(
        blank=True,
        default=0,
        help_text="Grade of the first user in the match."
    )
    username2_grade = models.IntegerField(
        blank=True,
        default=0,
        help_text="Grade of the second user in the match."
    )
    match_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='match',
        help_text="Type of match, either tournament or one-to-one."
    )

    def __str__(self):
        return f"{self.match_username1} vs {self.match_username2}"
