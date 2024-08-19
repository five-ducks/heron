from django.contrib import admin
from games.models import Match, Tournament

@admin.register(Match)
@admin.register(Tournament)

class MatchAdmin(admin.ModelAdmin):
    pass

class TournamentAdmin(admin.ModelAdmin):
    pass
