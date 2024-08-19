from django.db import models

class User(models.Model):

    PROFILE_IMGS = [
        (1, '피카츄'),
        (2, '이상해씨'),
        (3, '파이리'),
        (4, '잉어킹'),
    ]

    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    profile_img = models.IntegerField(choices=PROFILE_IMGS, default=1)
    exp = models.IntegerField(default=0)
    macrotext1 = models.CharField(max_length=20, blank=True, default="good game")
    macrotext2 = models.CharField(max_length=20, blank=True, default="thanks")
    macrotext3 = models.CharField(max_length=20, blank=True, default="bye bye")
    macrotext4 = models.CharField(max_length=20, blank=True, default="goooooood!")
    macrotext5 = models.CharField(max_length=20, blank=True, default="hello")

    def __str__(self):
        return self.user_profile_nickname