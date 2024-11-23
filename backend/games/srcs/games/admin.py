from django.contrib import admin
from games.models import Match

@admin.register(Match)

class MatchAdmin(admin.ModelAdmin):
    pass
