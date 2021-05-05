from django.urls import path

from activities.views import get_ranking, home

urlpatterns = [
    path('', get_ranking, name='get_ranking'),
]