from django.shortcuts import render
from mainpage.models import Tournaments, TournamentParticipation, Fighters, TournamentNominations
from mainpage.models import Divisions, Weapons
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

def tournaments_list(request):
    tournaments = Tournaments.objects.all()
    context = {
        'tournaments': tournaments,
    }
    return render(request, 'tournaments/tournaments_list.html', context)


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


def org_process_get(tournament):
    nominations = tournament.tournamentnominations_set.all()
    participation = tournament.tournamentparticipation_set.all()
    return {"status": status.HTTP_200_OK, "result": {
        "tournament": TournamentSerializer(tournament).data,
        'nominations': TournamentNominationsSerializer(nominations, many=True).data,
        'participation': TournamentParticipationSerializer(participation, many=True).data}
            }


def fighter_add(tournament, data):
    try:
        fighter = Fighters.objects.get(id=data["fighter"], active=True)
    except Fighters.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Боец с таким id в базе отсутствует или неактивен"}

    try:
        nomination = TournamentNominations.objects.get(id=data["nomination"])
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


def fighter_confirm(tournament, data):
    try:
        participation = TournamentParticipation.objects.get(id=data["participation"])
    except TournamentParticipation.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой записи об участии в турнире с базе не значится"}

    participation.confirmed = True
    participation.save()
    return {"status": status.HTTP_200_OK, "result": TournamentParticipationSerializer(participation).data}


def nomination_add(tournament, data):
    try:
        division = Divisions.objects.get(id=data['division'], deprecated=False)
    except Divisions.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой эшелон базе отсутствует"}

    try:
        weapon = Weapons.objects.get(id=data['weapon'], deprecated=False)
    except Weapons.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой вид вооружения базе отсутствует"}

    try:
        TournamentNominations.objects.get(tournament=tournament, division=division, weapon=weapon, gender=data['gender'])
        return {"status": status.HTTP_409_CONFLICT, "result": "Такая номинация уже существует"}
    except TournamentNominations.DoesNotExist:
        nomination = TournamentNominations(tournament=tournament, division=division, weapon=weapon, gender=data['gender'])
        nomination.save()
        return {"status": status.HTTP_200_OK, "result": TournamentNominationsSerializer(nomination).data}


def nomination_correct(tournament, data):
    try:
        nomination = TournamentNominations.objects.get(id=data["nomination"])
    except TournamentNominations.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Номинация с таким id в базе отсутствует"}
    if data.get('division'):
        try:
            division = Divisions.objects.get(id=data['division'], deprecated=False)
            nomination.division = division
        except Divisions.DoesNotExist:
            return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой эшелон базе отсутствует"}

    if data.get('weapon'):
        try:
            weapon = Weapons.objects.get(id=data['weapon'], deprecated=False)
            nomination.weapon = weapon
        except Weapons.DoesNotExist:
            return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой вид вооружения базе отсутствует"}

    if data.get('gender'):
        nomination.gender = data.get('gender')

    nomination.save()
    return {"status": status.HTTP_200_OK, "result": TournamentNominationsSerializer(nomination).data}


def tournament_delete(tournament, data):
    return {"status": status.HTTP_200_OK, "result": tournament.delete()}


def tournament_correct(tournament, data):
    parameters_list = ('name', 'city', 'start_date', 'end_date', 'description', 'rules_text', 'rules_json')
    for parameter in parameters_list:
        if data.get(parameter):
            setattr(tournament, parameter, data.get(parameter))

    if tournament.start_date > tournament.end_date:
        return {"status": status.HTTP_417_EXPECTATION_FAILED, "result": {'Дата начала турнира не может быть позже даты его окончания'}}

    tournament.save()
    return {"status": status.HTTP_200_OK, "result": TournamentSerializer(tournament).data}


def nomination_delete(tournament, data):
    try:
        nomination = TournamentNominations.objects.get(id=data["nomination"])
    except TournamentNominations.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Номинация с таким id в базе отсутствует"}

    return {"status": status.HTTP_200_OK, "result": nomination.delete()}


def participation_delete(tournament, data):
    try:
        participation = TournamentParticipation.objects.get(id=data["participation"])
    except TournamentParticipation.DoesNotExist:
        return {"status": status.HTTP_404_NOT_FOUND, "result": "Такой записи об участии в турнире с базе не значится"}

    return {"status": status.HTTP_200_OK, "result": participation.delete()}


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def tournament_manipulation_org(request, pk):
    routing = {
        'GET': org_process_get,
        'PUT': {
            'fighter-confirm': fighter_confirm,
            'nomination-correct': nomination_correct,
            'tournament-correct': tournament_correct,
        },
        'POST': {
            'fighter-add': fighter_add,
            'fighter-confirm': fighter_confirm,
            'nomination-add': nomination_add,
            'nomination-correct': nomination_correct,
        },
        'DELETE': {
            'delete-tournament': tournament_delete,
            'delete-nomination': nomination_delete,
            'delete-participation': participation_delete,
        },
    }
    try:
        tournament = Tournaments.objects.get(id=pk)
    except Tournaments.DoesNotExist:
        return Response("Турнир с таким id в базе отсутствует", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        result = routing[request.method](tournament)
    else:
        result = routing[request.method][request.data['command']](tournament, request.data['data'])

    return Response(result['result'], status=result['status'])
