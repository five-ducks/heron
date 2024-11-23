from django.contrib.auth.models import AbstractUser
from django.db import models

##### max_length에 대한 설명 #####
# CharField는 VARCHAR 형식을 사용합니다
# VARCHAR 형식은 가변길이 문자열로 최대 길이만 설정해놓으면 해당 길이 이내의 문자열을 가변적으로 저장할 수 있습니다
# 또한, 현재 Database는 utf8 인코딩 방식을 사용중이며 1개의 문자당 1~4byte가 사용됩니다.
# 따라서 max_length=n 인 경우 최대 n개의 문자를 저장할 수 있습니다.
# '1' / '김' / 'a' 도 모두 동일하게 1개의 문자로 취급합니다.

class Auth(AbstractUser):
    
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="User unique id"
    )
    ## username에 대한 필드 설정입니다.
    ## 최대 150문자까지 저장 가능합니다.

    def __str__(self):
        return f"{self.username}"