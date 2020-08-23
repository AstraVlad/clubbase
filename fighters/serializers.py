from rest_framework import serializers
from mainpage.models import Fighters


class FighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighters
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'city', 'date_of_birth']
