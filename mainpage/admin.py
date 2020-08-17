from django.contrib import admin
from .models import Clubs, Fighters, Tournaments

# Register your models here.
admin.site.register(Clubs)
admin.site.register(Fighters)
admin.site.register(Tournaments)
