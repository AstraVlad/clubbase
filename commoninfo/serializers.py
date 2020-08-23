from rest_framework import serializers
from mainpage.models import Weapons, Divisions


class WeaponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapons
        fields = ['id', 'name', 'deprecated']

class DivisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisions
        fields = ['id', 'name', 'deprecated']
