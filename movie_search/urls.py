from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("home/", views.home, name='home'),
    path("movies_popular/", views.movies_popular, name='movies_popular'),
    path("movies_top_rated/", views.movies_top_rated, name='movies_top_rated'),
    path("movies_now_playing/", views.movies_now_playing, name='movies_now_playing'),
    path("movies_upcoming/", views.movies_upcoming, name='movies_upcoming'),
    path("movies_trending_week/", views.movies_trending_week, name='movies_trending_week'),
    path("media_similar/", views.media_similar, name='media_similar'),
    path("error/", views.media_similar, name='error'),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("tv/<int:tv_id>/", views.tv_detail, name="tv_detail"),
]