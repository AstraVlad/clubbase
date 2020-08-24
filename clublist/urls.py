from django.urls import path
from . import views
from .views import ClubListView, ClubView


urlpatterns = [
    path('', views.clubs_list),
    path('api/<int:pk>/', ClubView.as_view()),
    path('api/', ClubListView.as_view()),
    path('<int:pk>/', views.club_details),

]
