from django.urls import path
from .views import index,detail,studio,anime_studio,advance_search,advance_data

urlpatterns = [
    #Menambahkan path sesuai dengan urls
    path('', index, name='index'),
    path('detail', detail, name='detail'),
    path('studio', studio, name='studio'),
    path('anime-studio', anime_studio, name='anime-studio'),
    path('advance',advance_search, name = 'advance'),
    path('advance-data',advance_data, name = 'advance_data')
]