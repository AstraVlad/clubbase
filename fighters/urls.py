from django.urls import path
from . import views
from .views import FighterView, FightersListView

urlpatterns = [
    path('', views.fighters_list),
    path('api/', FightersListView.as_view()),
    path('api/<int:pk>/', FighterView.as_view()),
    path('<int:pk>/', views.fighter_detail),
    # path('newfighter/', views.fighter_new),
]
