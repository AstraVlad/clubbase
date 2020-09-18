from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.forms.widgets import PasswordInput
# from django.contrib.auth.decorators import login_required


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
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': PasswordInput(),
        }


def users_add(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = form.save()
            # username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            # redirect to a new URL:
            return HttpResponseRedirect('/fighters/add/')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = UserCreationForm()
    return render(request, 'users/add_user.html', {'form': form})
