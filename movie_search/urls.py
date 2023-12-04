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
    path("tv/<int:tv_id>/", views.tv_detail, name="tv_detail"),
    path("media_search/", views.search, name="media_search"),
    path("error/", views.search, name="error"),
    path("discover/movie/", views.discover_movie, name="discover_movie"),
    path('watch_list/add/<int:movie_id>/', views.add_to_watch_list, name='add_to_watch_list'),
    path('watch_list/remove/<int:movie_id>/', views.remove_from_watch_list, name='remove_from_watch_list'),
    path('watch_list/', views.watch_list, name='watch_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
