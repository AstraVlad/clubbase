from django.urls import path
from . import views
from .views import FighterView, FightersListView

urlpatterns = [
    path('', views.fighters_list, name='fighters_list'),
    path('api/', FightersListView.as_view()),
    path('api/<int:pk>/', FighterView.as_view()),
    path('<int:pk>/', views.fighter_detail, name='fighter_detail'),
    path('edit/', views.fighter_edit, name='fighter_edit'),
    path('add/', views.fighter_add, name='fighter_add'),
]
