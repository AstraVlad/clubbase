from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.forms import ModelForm
from mainpage.models import Fighters
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.forms.widgets import PasswordInput, CheckboxSelectMultiple, ClearableFileInput
from django.http import Http404
from django.contrib.auth.decorators import login_required


# Create your views here.
@api_view(['POST'])
def api_user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"user": user}, status=status.HTTP_200_OK)
    else:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def api_user_logout(request):
    logout(request)
    return Response({}, status=status.HTTP_200_OK)


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields =['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': PasswordInput(),
        }


class FighterForm(ModelForm):
    class Meta:
        model = Fighters
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'city', 'date_of_birth',
                  'current_club', 'division', 'weapons', 'gender', 'userpic']
        widgets = {
            'weapons': CheckboxSelectMultiple(),
            'userpic': ClearableFileInput(),
        }


def users_add_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = form.save()
            user.groups.add(Group.objects.get(name='Fighters'))
            user.save()
            login(request, user)
            #new_id = user.pk
            print(f'/fighter/{user.groups}')
            # redirect to a new URL:
            return HttpResponseRedirect(f'/users/add/fighter/')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = UserCreationForm()

    return render(request, 'users/add_user.html', {'form': form})


def add_fighter(request, user):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FighterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            fighter = form.save()
            fighter.user = user
            fighter.save()
            # new_id = user.pk
            # redirect to a new URL:
            return HttpResponseRedirect('/')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = FighterForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})

    return render(request, 'users/add_fighter.html', {'form': form})


@login_required()
def users_add_fighter(request):
    user = request.user
    if hasattr(user, 'fighter'):
        return HttpResponseRedirect('/')
    else:
        return add_fighter(request, user)
