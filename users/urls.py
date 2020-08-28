from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.api_user_login),
    path('api/logout/', views.api_user_logout),
    path('add/', views.users_add_user, name='user_add'),
    path('add/fighter/', views.users_add_fighter, name='fighter_add'),
]
