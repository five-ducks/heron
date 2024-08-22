from django.db import models
from users.models import User

class Friend(models.Model):

    STATUS_CHOICES = [
        ('pending', '대기상태'),
        ('accepted', '친구상태'),
    ]

    user1_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends_initiated',
        help_text="Reference to the initiating user in the friend request."
    )
    user2_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends_received',
        help_text="Reference to the receiving user in the friend request."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the friend request."
    )

    def __str__(self):
        return f"{self.user1_id.username} - {self.user2_id.username} ({self.status})"
