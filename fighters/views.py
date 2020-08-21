from django.shortcuts import render
from mainpage.models import Fighters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import FighterSerializer


# Create your views here.

def fighters_list(request):
    fighters = Fighters.objects.all()
    return render(request, 'fighters/fighters_list.html', {'fighters': fighters})

def fighter_detail(request, pk):
    try:
        fighter = Fighters.objects.get(id=pk)
    except Fighters.DoesNotExist:
        context = {
            'result': 0,
        }

    context = {
        'result': 1,
        'fighter': fighter,
    }

    return render(request, 'fighters/fighter_details.html', context)


class FighterView(APIView):
    def get_object(self, pk):
        try:
            return Fighters.objects.get(id=pk)
        except Fighters.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        fighter = self.get_object(pk)
        serializer = FighterSerializer(fighter)
        return Response({'fighter': serializer.data})