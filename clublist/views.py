from django.shortcuts import render
from mainpage.models import Club
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClubListSerializer



def clubs_list(request):
    clubs = Club.objects.all()
    clubs_string = ''
    for club in clubs:
        clubs_string += f'<a href="{club.id}">{club}</a><br>'

    context = {
        'clublist': clubs_string,
    }

    return render(request, 'clublist/clubs_list.html', context)


def club_details(request, pk):
    club = Club.objects.filter(id__exact=pk)
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
        clubs = Club.objects.all()
        serializer = ClubListSerializer(clubs, many=True)
        return Response({'clubs': serializer.data})
