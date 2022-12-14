from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("movies_popular/", views.movies_popular, name="movies_popular"),
    path("movies_top_rated/", views.movies_top_rated, name="movies_top_rated"),
    path("movies_trending_week/", views.movies_trending_week, name="movies_trending_week"),
    path("movies_now_playing/", views.movies_now_playing, name="movies_now_playing"),
    path("movies_upcoming/", views.movies_upcoming, name="movies_upcoming"),
    path("movie/<int:obj_id>/", views.movie_detail, name="movie_detail"),
    path("tv_popular/", views.tv_popular, name="tv_popular"),
    path("tv_top_rated/", views.tv_top_rated, name="tv_top_rated"),
    path("tv_trending_week/", views.tv_trending_week, name="tv_trending_week"),
    path("tv_air/", views.tv_air, name="tv_air"),
    path("tv_air_today/", views.tv_air_today, name="tv_air_today"),
    path("tv/<int:obj_id>/", views.tv_detail, name="tv_detail"),
    path("media_search/", views.search, name="media_search"),
    path("person_search/", views.search, name="person_search"),
    path("error/", views.search, name="error"),
    path("discover/movie/", views.discover, name="discover"),
]
