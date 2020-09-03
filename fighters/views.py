from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .serializers import FighterSerializer
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from mainpage.models import Fighters
from django.forms.widgets import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
# Create your views here.


class FighterForm(ModelForm):
    class Meta:
        model = Fighters
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'city', 'date_of_birth',
                  'current_club', 'division', 'weapons', 'gender', 'userpic']
        widgets = {
            'weapons': CheckboxSelectMultiple(),
        }


# Показываем список бойцов

def fighters_list(request):
    fighters = Fighters.objects.all().exclude(active=False)
    return render(request, 'fighters/fighters_list.html', {'fighters': fighters})


# Показываем информацию о конкретном бойце
def fighter_detail(request, pk):
    try:
        fighter = Fighters.objects.get(id=pk, active=True)
        user_fighter = getattr(request.user, 'fighter', False)
        edit = False
        if user_fighter and user_fighter.id == pk:
            edit = True
        context = {
            'result': 1,
            'fighter': fighter,
            'edit': edit,
        }
    except Fighters.DoesNotExist:
        context = {
            'result': 0,
        }

    return render(request, 'fighters/fighter_details.html', context)


# Добавляем запись о бойце для текущего пользователя
@login_required()
def fighter_add(request):
    user = request.user
    if hasattr(user, 'fighter'):
        print(getattr(user, 'fighter'))
        return HttpResponseRedirect('/')
    else:
        fighter = Fighters(user=user, first_name=user.first_name, last_name=user.last_name, email=user.email)
        fighter.save()
        # Редирект на редактирование свежесозданной записи
        return HttpResponseRedirect("/fighters/edit/")


# Редактируем информацию о конкретном бойце
@login_required()
def fighter_edit(request):
    fighter = getattr(request.user, 'fighter', False)
    if not fighter:
        return render(request, 'error.html',
                      {'error': 'Текущему пользователю не сопоставлена запись бойца!'})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FighterForm(request.POST, request.FILES, instance=fighter)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            print(request.FILES)
            # fighter.save()
            # Редирект на отображение свежесозданной записи
            return HttpResponseRedirect(f'/fighters/{request.user.fighter.id}')
    else:
        form = FighterForm(instance=fighter)

    return render(request, 'fighters/fighter_edit.html', {'form': form})


class FighterView(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Fighters.objects.get(id=pk, active=True)
        except Fighters.DoesNotExist:
            raise Http404

    @staticmethod
    def check_owner(fighter, request):
        if not (fighter.user == request.user or (request.user.is_staff and request.user.is_active)):
            raise PermissionDenied

    def get(self, request, pk):
        fighter = self.get_object(pk)
        serializer = FighterSerializer(fighter)
        return Response({'fighter': serializer.data})

    @login_required
    def put(self, request, pk):
        fighter = self.get_object(pk)
        self.check_owner(fighter, request)
        serializer = FighterSerializer(fighter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def delete(self, request, pk):
        fighter = self.get_object(pk)
        self.check_owner(fighter, request)
        fighter.active = False
        fighter.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FightersListView(generics.ListAPIView):
    queryset = Fighters.objects.all().exclude(active=False)
    serializer_class = FighterSerializer
