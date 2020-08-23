from rest_framework import serializers
from mainpage.models import Clubs


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubs
        fields = ['id', 'long_name', 'short_name', 'city', 'description']
