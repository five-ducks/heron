from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

# @admin.register(User)

# class CustomUserAdmin(UserAdmin):
#     add_fieldsets = (
#         (
#             None, {
#                 'classes': ('wide',),
#                 'fields': ('username', 'password1', 'password2', 'profile_img'),
#             }
#         ),
#     )
#     ## django-admin 에서 user테이블 필드 생성시 필수적으로 입력해야하는 field를 정의합니다.
    
#     fieldsets = [
#         (
#             None, {
#                 "fields": ("username", "password")
#             }
#         ),
#         (
#             "프로필정보", { 
#                 "fields": ("profile_img", "status_msg")
#             }
#         ),
#         (
#             "상태정보", {
#                 "fields": ("status",)
#             }
#         ),
#         (
#             "게임통계", {
#                 "fields": ("exp", "win_cnt", "lose_cnt")
#             },
#         ),
#         (
#             "매크로텍스트",
#             {
#                 "fields": ("macrotext1", "macrotext2", "macrotext3", "macrotext4", "macrotext5")
#             }
#         ),
#         (
#             "권한",
#             {
#                 "fields": ("is_active", "is_staff", "is_superuser")
#             },
#         )
#     ]
#     ## django-admin에서 생성 및 수정을 진행하고 싶은 field를 정의합니다.

# ## UserAdmin은 django admin에서 확인할 DB 필드를 정의해놓은 것입니다.