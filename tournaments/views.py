from django.shortcuts import render
from mainpage.models import Tournaments
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import TournamentSerializer, TournamentNominationsSerializer, TournamentParticipationSerializer

# Create your views here.

class TournamentsList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Tournaments.objects.all()
    serializer_class = TournamentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TournamentsListOrg(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Tournaments.objects.all()
    serializer_class = TournamentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TournamentDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Tournaments.objects.all()
    serializer_class = TournamentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def orgProcessGet(request, pk):
    tournament = Tournaments.objects.get(id=pk)
    nominations = tournament.tournamentnominations_set.all()
    participation = tournament.tournamentparticipation_set.all()
    return {"tournament": TournamentSerializer(tournament).data,
    'nominations': TournamentNominationsSerializer(nominations, many=True).data,
    'participation': TournamentParticipationSerializer(participation, many=True).data}

def orgProcessPost(request, pk):
    return Response({"metod": "Post"})

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def TournamentDetailOrg(request, pk):
    if request.method == 'GET':
        result = orgProcessGet(request, pk)
    elif request.method == 'POST':
        result = orgProcessPost(request, pk)

    return Response(result)
