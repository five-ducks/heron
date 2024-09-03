from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        (
            "추가필드", 
            {
                "fields": (
                    "profile_img",
                    "status",
                    "exp",
                    "win_cnt",
                    "lose_cnt",
                    "status_msg"
                )
            }
        ),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("중요한 일정", {"fields": ("last_login", "date_joined")}),
    ]
