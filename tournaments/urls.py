from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tournaments import views

urlpatterns = [
    path('api/<int:pk>', views.TournamentDetail.as_view()),
    path('api/', views.TournamentsList.as_view()),
    path('api/org/<int:pk>', views.TournamentDetailOrg),
    path('api/org/', views.TournamentsListOrg.as_view()),
]
