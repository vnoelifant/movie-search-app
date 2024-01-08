from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("movie_popular/", views.movies_popular, name="movies_popular"),
    path("movie_top_rated/", views.movies_top_rated, name="movies_top_rated"),
    path("movie_trending_week/", views.movies_trending_week, name="movies_trending_week"),
    path("movie_now_playing/", views.movies_now_playing, name="movies_now_playing"),
    path("movie_upcoming/", views.movies_upcoming, name="movies_upcoming"),
    path("movie/<int:movie_id>/", views.movie, name="movie"),
    path("tv_popular/", views.tv_popular, name="tv_popular"),
    path("tv_top_rated/", views.tv_top_rated, name="tv_top_rated"),
    path("tv_trending_week/", views.tv_trending_week, name="tv_trending_week"),
    path("tv_air/", views.tv_air, name="tv_air"),
    path("tv_air_today/", views.tv_air_today, name="tv_air_today"),
    path("tv/<int:series_id>/", views.tv, name="tv"),
    path("media_search/", views.search, name="media_search"),
    path("error/", views.search, name="error"),
    path("discover/movie/", views.movie_discover, name="movie_discover"),
    path('movie_watch_list/add/<int:movie_id>/', views.add_movie_to_watch_list, name='add_movie_to_watch_list'),
    path('movie_watch_list/remove/<int:movie_id>/', views.remove_movie_from_watch_list, name='remove_movie_from_watch_list'),
    path('movie_watch_list/', views.movie_watch_list, name='movie_watch_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
