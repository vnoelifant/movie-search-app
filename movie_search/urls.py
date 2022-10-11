from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("home/", views.home, name='home'),
    path("movies_popular/", views.movies_popular, name='movies_popular'),
    path("movies_top_rated/", views.movies_top_rated, name='movies_top_rated'),
    path("media_similar/", views.media_similar, name='media_similar'),
    path("media_recommended/", views.media_recommended, name='media_recommended'),
    path("error/", views.media_similar, name='error'),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
]