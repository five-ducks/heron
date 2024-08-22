from django.db import models

class User(models.Model):

    PROFILE_IMGS = [
        (1, '피카츄'),
        (2, '이상해씨'),
        (3, '파이리'),
        (4, '잉어킹'),
    ]

    username = models.CharField(
        max_length=10,
        help_text="Username used as the login ID for the user."
    )
    password = models.CharField(
        max_length=20,
        help_text="Password for the user login."
    )
    nickname = models.CharField(
        max_length=10,
        help_text="Nickname for the user."
    )
    profile_img = models.IntegerField(
        choices=PROFILE_IMGS,
        default=1,
        help_text="Profile image ID for the user, selectable from predefined options."
    )
    exp = models.IntegerField(
        default=0,
        help_text="Experience points accumulated by the user."
    )
    macrotext1 = models.CharField(
        max_length=20,
        blank=True,
        default="good game",
        help_text="Macro text 1, default is 'good game'."
    )
    macrotext2 = models.CharField(
        max_length=20,
        blank=True,
        default="thanks",
        help_text="Macro text 2, default is 'thanks'."
    )
    macrotext3 = models.CharField(
        max_length=20,
        blank=True,
        default="bye bye",
        help_text="Macro text 3, default is 'bye bye'."
    )
    macrotext4 = models.CharField(
        max_length=20,
        blank=True,
        default="goooooood!",
        help_text="Macro text 4, default is 'goooooood!'."
    )
    macrotext5 = models.CharField(
        max_length=20,
        blank=True,
        default="hello",
        help_text="Macro text 5, default is 'hello'."
    )

    def __str__(self):
        return f"{self.username} ({self.nickname})"
