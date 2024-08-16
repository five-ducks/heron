from django.contrib import admin
from friends.models import Friend

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
