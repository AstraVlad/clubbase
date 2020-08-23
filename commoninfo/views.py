from django.shortcuts import render
from mainpage.models import Weapons, Divisions
from rest_framework import generics
from .serializers import WeaponsSerializer, DivisionsSerializer

# Create your views here.


def weapons_list(request):
    weapons = Weapons.objects.all()
    context = {
        'weapons': weapons,
    }
    return render(request, 'commoninfo/weapons_list.html', context)


def divisions_list(request):
    divisions = Divisions.objects.all()
    context = {
        'divisions': divisions,
    }
    return render(request, 'commoninfo/divisions_list.html', context)

class WeaponsList(generics.ListAPIView):
    queryset = Weapons.objects.all()
    serializer_class = WeaponsSerializer


class DivisionsList(generics.ListAPIView):
    queryset = Divisions.objects.all()
    serializer_class = DivisionsSerializer
