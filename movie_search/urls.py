from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("search/", views.search, name='search'),
    path("movies/", views.movies, name='movies')
]