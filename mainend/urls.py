from django.urls import path
from .views import index,detail,studio,anime_studio,advance_search

urlpatterns = [
    #Menambahkan path sesuai dengan urls
    path('', index, name='index'),
    path('detail', detail, name='detail'),
    path('studio', studio, name='studio'),
    path('anime-studio', anime_studio, name='anime-studio'),
    path('advance',advance_search, name = 'advance')
]