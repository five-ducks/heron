from django.contrib import admin
from users.models import User, Image

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass