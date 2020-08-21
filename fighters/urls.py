from django.urls import path
from . import views
from .views import FighterView

urlpatterns = [
    path('', views.fighters_list),
    path('api/<int:pk>/', FighterView.as_view()),
    path('<int:pk>/', views.fighter_detail),
]
