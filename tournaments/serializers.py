from rest_framework import serializers
from mainpage.models import Tournaments, TournamentNominations, TournamentParticipation


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = ['pk', 'name', 'city', 'start_date', 'end_date', 'description', 'rules_text', 'rules_json']

class TournamentNominationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentNominations
        fields = ['pk', 'tournament', 'division', 'weapon', 'gender']

class TournamentParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipation
        fields = ['pk', 'fighter', 'tournament', 'nomination', 'got_a_place', 'was_disqualified']
