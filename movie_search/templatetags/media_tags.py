import json

from django import template

from movie_search.models import MovieGenre, MovieProvider, TVSeriesGenre, TVSeriesProvider

register = template.Library()


@register.simple_tag
def get_movie_genres():
    movie_genre_names = MovieGenre.objects.values_list('name', flat=True)
    return movie_genre_names

@register.simple_tag
def get_movie_providers():
    movie_provider_names = MovieProvider.objects.values_list('name', flat=True)
    return movie_provider_names

@register.simple_tag
def get_tv_genres():
    tv_genre_names = TVSeriesGenre.objects.values_list('name', flat=True)
    return tv_genre_names

@register.simple_tag
def get_tv_providers():
    tv_provider_names = TVSeriesProvider.objects.values_list('name', flat=True)
    return tv_provider_names