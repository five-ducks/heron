from django.db import models

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', null=True)

class User(models.Model):
    user_login_id = models.CharField(max_length=10)
    user_login_password = models.CharField(max_length=20)
    user_profile_nickname = models.CharField(max_length=10)
    user_image_id = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    user_macrotext1 = models.CharField(max_length=20, blank=True, null=True, default="good game")
    user_macrotext2 = models.CharField(max_length=20, blank=True, null=True, default="thanks")
    user_macrotext3 = models.CharField(max_length=20, blank=True, null=True, default="bye bye")
    user_macrotext4 = models.CharField(max_length=20, blank=True, null=True, default="goooooood!")
    user_macrotext5 = models.CharField(max_length=20, blank=True, null=True, default="hello")

    def __str__(self):
        return self.user_profile_nickname