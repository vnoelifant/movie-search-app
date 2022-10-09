from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("home/", views.home, name='home'),
    path("movies_popular/", views.movies_popular, name='movies_popular'),
    path("movies_top_rated/", views.movies_top_rated, name='movies_top_rated'),
    path("movies_similar/", views.movies_similar, name='movies_similar'),
    path("error/", views.movies_similar, name='error'),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
]