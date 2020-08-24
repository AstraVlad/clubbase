from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from .views import WeaponsList, DivisionsList, weapons_list, divisions_list, api_info

urlpatterns = [
    path('weapons/api/', WeaponsList.as_view()),
    path('divisions/api/', DivisionsList.as_view()),
    path('weapons/', weapons_list),
    path('divisions/', divisions_list),
    path('apiinfo/', api_info),
]
