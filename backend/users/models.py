from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    PROFILE_IMGS = [
        (0, '피카츄'),
        (1, '파이리'),
        (2, '이상해씨'),
        (3, '꼬부기'),
        (4, '이브이'),
        (5, '잠만보'),
        (6, '뮤'),
        (7, '메타몽'),
    ]
    STATUS_CHOICES = [
        (0, '오프라인'),
        (1, '온라인'),
        (2, '게임중'),
    ]
    STATUS_MAP = {label: value for value, label in STATUS_CHOICES}
    # label을 통해 field값을 설정하기 위한 맵입니다.
    
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[],
        error_messages={
            "unique": ("사용중인 username 입니다"),
        },
    )
    profile_img = models.IntegerField(
        choices=PROFILE_IMGS,
        default=0,
        help_text="Profile image ID for the user, selectable from predefined options."
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        help_text="User activity status"
    )
    exp = models.IntegerField(
        default=0,
        help_text="Experience points accumulated by the user."
    )
    win_cnt = models.IntegerField(
        default=0,
        help_text="User win count"   
    )
    lose_cnt = models.IntegerField(
        default=0,
        help_text="User lose count"   
    )
    status_msg = models.CharField(
        null=True,
        blank=True,
        help_text="User custom status message"
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
        return f"{self.username}"
