from django.db import models
from users.models import User

class Friend(models.Model):

    STATUS_CHOICES = [
        ('pending', '대기상태'),  # ('저장되는 값', '사람이 읽기 쉬운 레이블')
        ('accepted', '친구상태'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fuser_id')
    friend_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_id')
    friend_relation = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
