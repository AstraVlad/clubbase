from rest_framework import serializers
from mainpage.models import Club


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'long_name', 'short_name', 'city', 'description']
