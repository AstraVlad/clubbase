from rest_framework import serializers
from mainpage.models import Clubs


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubs
        fields = ['id', 'long_name', 'short_name', 'city', 'description']
