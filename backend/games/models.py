from django.utils import timezone

from django.db import models
from users.models import User

class Match(models.Model):

    RESULT_CHOICES = [
        ('user_win', '사용자 승리'),
        ('opponent_win', '상대방 승리'),
        ('pending_result', '결과 대기중'),
    ]

    TYPE_CHOICES = [
        ('tournament', '토너먼트 경기'),
        ('match', '1대1경기'),
    ]

    user1_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='matches_as_user1',
        help_text="Reference to the first user participating in the match."
    )
    user2_id = models.ForeignKey(
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
    user1_grade = models.IntegerField(
        blank=True,
        default=0,
        help_text="Grade of the first user in the match."
    )
    user2_grade = models.IntegerField(
        blank=True,
        default=0,
        help_text="Grade of the second user in the match."
    )
    match_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='match',
        help_text="Type of match, either tournament or one-on-one."
    )

    def __str__(self):
        return f"{self.user1_id} vs {self.user2_id}"


class Tournament(models.Model):
    semifinal1 = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
        related_name='semifinal_matches1',
        help_text="Reference to the first semifinal match."
    )
    semifinal2 = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
        related_name='semifinal_matches2',
        help_text="Reference to the second semifinal match."
    )
    bonus_match = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
        related_name='bonus_matches',
        help_text="Reference to the bonus match."
    )
    final = models.ForeignKey(
        'Match',
        on_delete=models.CASCADE,
        related_name='final_matches',
        help_text="Reference to the final match."
    )

    def __str__(self):
        return f"Tournament with matches: {self.semifinal1}, {self.semifinal2}, {self.bonus_match}, {self.final}"
