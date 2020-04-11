from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('addmovie/', views.addmovie),
    path('addmovie/search', views.search),
    path('moviedetails/', views.moviedetails),
    path('moviedetails/watchtrailer', views.watchtrailer),
    path('moviedetails/playmovie', views.playmovie),
    #path('favourites/', views.favourites),
    
]