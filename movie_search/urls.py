from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("movies_popular/", views.movies_popular, name='movies_popular'),
    path("movies_top_rated/", views.movies_top_rated, name='movies_top_rated')
]