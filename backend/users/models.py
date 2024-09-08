from django.contrib.auth.models import AbstractUser
from django.db import models

##### max_length에 대한 설명 #####
# CharField는 VARCHAR 형식을 사용합니다
# VARCHAR 형식은 가변길이 문자열로 최대 길이만 설정해놓으면 해당 길이 이내의 문자열을 가변적으로 저장할 수 있습니다
# 또한, 현재 Database는 utf8 인코딩 방식을 사용중이며 1개의 문자당 1~4byte가 사용됩니다.
# 따라서 max_length=n 인 경우 최대 n개의 문자를 저장할 수 있습니다.
# '1' / '김' / 'a' 도 모두 동일하게 1개의 문자로 취급합니다.

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
    ## profile_img를 enum으로 관리하기 위한 조건입니다.
    
    STATUS_CHOICES = [
        (0, '오프라인'),
        (1, '온라인'),
        (2, '게임중'),
    ]
    STATUS_MAP = {label: value for value, label in STATUS_CHOICES}
    ## label을 통해 field값을 설정하기 위한 맵입니다.
    
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[],
        help_text="User unique id"
    )
    ## username에 대한 필드 설정입니다.
    ## 최대 150문자까지 저장 가능합니다.
    
    profile_img = models.IntegerField(
        choices=PROFILE_IMGS,
        default=0,
        help_text="Profile image ID for the user, selectable from predefined options."
    )
    ## 프로필 이미지에 대한 필드 설정입니다.
    ## 기본값은 0 입니다.
    ## PROFILE_IMGS에 저장된 ENUM을 통해 관리됩니다.
    
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        help_text="User activity status"
    )
    ## 유저상태에 대한 필드 설정입니다.
    ## 기본값은 0 입니다.
    ## STATUS_CHOICES에 저장된 ENUM을 통해 관리됩니다.
    
    exp = models.IntegerField(
        default=0,
        help_text="Experience points accumulated by the user."
    )
    ## 경험치에 대한 필드 설정입니다.
    ## 기본값은 0 입니다.
    
    win_cnt = models.IntegerField(
        default=0,
        help_text="User win count"  
    )
    ## 승리횟수에 대한 필드 설정입니다.
    ## 기본값은 0 입니다.
    
    lose_cnt = models.IntegerField(
        default=0,
        help_text="User lose count"   
    )
    ## 패배횟수에 대한 필드 설정입니다.
    ## 기본값은 0 입니다.
    
    status_msg = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="User custom status message, default is '텍스트를 입력해주세요'"
    )
    ## 상태메세지에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.
    
    macrotext1 = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="Macro text 1, default is '텍스트를 입력해주세요'."
    )
    ## macrotext1에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.
    
    macrotext2 = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="Macro text 2, default is '텍스트를 입력해주세요'."
    )
    ## macrotext2에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.
    
    macrotext3 = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="Macro text 3, default is '텍스트를 입력해주세요'."
    )
    ## macrotext3에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.
    
    macrotext4 = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="Macro text 4, default is '텍스트를 입력해주세요'."
    )
    ## macrotext4에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.
    
    macrotext5 = models.CharField(
        max_length=100,
        blank=True,
        default="텍스트를 입력해주세요",
        help_text="Macro text 5, default is '텍스트를 입력해주세요'."
    )
    ## macrotext5에 대한 필드 설정입니다.
    ## 빈 입력을 허용합니다.
    ## 기본값은 '텍스트를 입력해주세요' 입니다.
    ## 최대 100 문자까지 저장 가능합니다.

    def __str__(self):
        return f"{self.username}"
