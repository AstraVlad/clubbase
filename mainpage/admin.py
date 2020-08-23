from django.contrib import admin
from .models import Clubs, Fighters, Tournaments, Weapons, Divisions, TournamentNominations, TournamentParticipation

# Register your models here.
admin.site.register(Clubs)
admin.site.register(Fighters)
admin.site.register(Tournaments)
admin.site.register(Weapons)
admin.site.register(Divisions)
admin.site.register(TournamentNominations)
admin.site.register(TournamentParticipation)
