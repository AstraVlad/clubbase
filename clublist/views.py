from django.shortcuts import render
from mainpage.models import Clubs
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClubSerializer
from rest_framework import status
from django.http import Http404


def clubs_list(request):
    clubs = Clubs.objects.all()
    context = {
        'clubs': clubs,
    }

    return render(request, 'clublist/clubs_list.html', context)


def club_details(request, pk):
    try:
        club = Clubs.objects.get(id=pk)
        fighters = club.fighters_set.all()
        context = {
            'club': f'{club.long_name}',
            'city': f'{club.city}',
            'description': f'{club.description}',
            'image': f'{club.get_emblem()}',
            'fighters': fighters,
        }
    except Clubs.DoesNotExist:
        context = {
            'club': 'Клуб с таким номером не найден',
            'city': '',
            'description': '',
            'image': '',
            'fighters': ''
        }

    return render(request, 'clublist/club_details.html', context)


class ClubListView(APIView):
    def get(self, request):
        clubs = Clubs.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response({'clubs': serializer.data})

    def post(self, request, format=None):
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClubView(APIView):
    def get_object(self, pk):
        try:
            return Clubs.objects.get(id=pk)
        except Clubs.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        club = self.get_object(pk)
        serializer = ClubSerializer(club)
        return Response({'Club': serializer.data})

    def put(self, request, pk, format=None):
        club = self.get_object(pk)
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        club = self.get_object(pk)
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
