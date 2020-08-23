# from django.shortcuts import render
from mainpage.models import Tournaments, TournamentParticipation, Fighters, TournamentNominations
# from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from .serializers import TournamentSerializer, TournamentNominationsSerializer, TournamentParticipationSerializer
from rest_framework import status


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
    try:
        tournament = Tournaments.objects.get(id=pk)
    except Tournaments.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Турнир с таким id в базе отсутствует"}
    nominations = tournament.tournamentnominations_set.all()
    participation = tournament.tournamentparticipation_set.all()
    return {"status": status.HTTP_200_OK, "result": {
        "tournament": TournamentSerializer(tournament).data,
        'nominations': TournamentNominationsSerializer(nominations, many=True).data,
        'participation': TournamentParticipationSerializer(participation, many=True).data}
            }


def fighterAdd(tournament, data):
    try:
        fighter = Fighters.objects.get(id=data["fighter-id"])
    except Fighters.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Боец с таким id в базе отсутствует"}

    try:
        nomination = TournamentNominations.objects.get(id=data["nomination-id"])
    except TournamentNominations.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Номинация с таким id в базе отсутствует"}

    try:
        TournamentParticipation.objects.get(fighter=fighter, nomination=nomination)
    except TournamentParticipation.DoesNotExist:
        participation = TournamentParticipation(fighter=fighter, tournament=tournament, nomination=nomination)
        participation.save()
        return {"status": status.HTTP_200_OK, "result": TournamentParticipationSerializer(participation).data}
    else:
        return {"status": status.HTTP_409_CONFLICT, "result": "Этот боец уже зарегистрирован в данной номинации"}


def fighterConfirm(tournament, data):
    try:
        fighter = Fighters.objects.get(id=data["fighter-id"])
    except Fighters.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Боец с таким id в базе отсутствует"}

    try:
        nomination = TournamentNominations.objects.get(id=data["nomination-id"])
    except TournamentNominations.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Номинация с таким id в базе отсутствует"}

    try:
        participation = TournamentParticipation.objects.get(fighter=fighter, nomination=nomination)
    except TournamentParticipation.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Боец с таким id на эту номинацию не заявлен"}

    # participation.confirmed = True
    return {"status": status.HTTP_200_OK, "result": 'Success'}


def nominationAdd(tournament, data):
    print(data)
    return 'NAdd'


def nominationCorrect(tournament, data):
    print(data)
    return 'NCorrect'


def orgProcessPost(request, pk):
    routing = {
        'fighter-add': fighterAdd,
        'fighter-confirm': fighterConfirm,
        'nomination-add': nominationAdd,
        'nomination-correct': nominationCorrect,
    }
    data = request.data
    try:
        tournament = Tournaments.objects.get(id=pk)
    except Tournaments.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Турнир с таким id в базе отсутствует"}
    result = routing[data["command"]](tournament, data["data"])

    return {"status": result['status'], "result": result['result']}


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def TournamentDetailOrg(request, pk):
    routing = {
        'GET': orgProcessGet,
        'PUT': orgProcessPost,
        'POST': orgProcessPost,
        'DELETE': 0,
    }
    result = routing[request.method](request, pk)
    return Response(result['result'], status=result['status'])
