from django.db import models
from users.models import User

class Friend(models.Model):

    username = models.ForeignKey(
        User,
        related_name="friends_as_username",
        null=True,
        on_delete=models.CASCADE,
        help_text="Reference to the initiating user in the friend request."
    )
    friendname = models.ForeignKey(
        User,
        related_name="friends_as_friendname",
        null=True,
        on_delete=models.CASCADE,
        help_text="Reference to the receiving user in the friend request."
    )

    def __str__(self):
        return f"{self.username} - {self.friendname}"
