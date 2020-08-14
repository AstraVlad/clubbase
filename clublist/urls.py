from django.urls import path
from . import views
from .views import ClubListView


urlpatterns = [
    path('', views.clubs_list),
    path('api/', ClubListView.as_view()),
    path('<int:pk>/', views.club_details),

]
