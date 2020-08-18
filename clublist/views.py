from django.shortcuts import render
from mainpage.models import Clubs
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClubListSerializer


def clubs_list(request):
    clubs = Clubs.objects.all()
    context = {
        'clubs': clubs,
    }

    return render(request, 'clublist/clubs_list.html', context)


def club_details(request, pk):
    club = Clubs.objects.filter(id__exact=pk)
    if len(club) == 0:
        context = {
            'club': 'Клуб не найден',
            'city': '',
            'description': '',
            'image': '',
        }
    for c in club:
        context = {
            'club': f'{c.long_name}',
            'city': f'{c.city}',
            'description': f'{c.description}',
            'image': f'{c.emblem.url}',
        }
    return render(request, 'clublist/club_details.html', context)


class ClubListView(APIView):
    def get(self, request):
        clubs = Clubs.objects.all()
        serializer = ClubListSerializer(clubs, many=True)
        return Response({'clubs': serializer.data})
