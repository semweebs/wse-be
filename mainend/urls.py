from django.urls import path
from .views import index

urlpatterns = [
    #Menambahkan path sesuai dengan urls
    path('', index, name='index'),
]