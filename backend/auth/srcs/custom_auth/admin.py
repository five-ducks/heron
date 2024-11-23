from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from custom_auth.models import Auth

@admin.register(Auth)

class AuthAdmin(UserAdmin):
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            }
        ),
    )
    ## django-admin 에서 user테이블 필드 생성시 필수적으로 입력해야하는 field를 정의합니다.
    
    fieldsets = [
        (
            None, {
                "fields": ("username", "password")
            }
        ),
        (
            "권한",
            {
                "fields": ("is_active", )
            },
        ),
    ]
    ## django-admin에서 생성 및 수정을 진행하고 싶은 field를 정의합니다.

## UserAdmin은 django admin에서 확인할 DB 필드를 정의해놓은 것입니다.