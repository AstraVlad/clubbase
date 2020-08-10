from django.urls import path
from . import views


urlpatterns = [
    path('', views.clubs_list),
    path('<int:pk>/', views.club_details),

]
