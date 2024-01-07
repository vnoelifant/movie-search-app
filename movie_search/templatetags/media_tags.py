import json

from django import template

from movie_search.models import MovieGenre, MovieProvider

register = template.Library()


@register.simple_tag
def get_movie_genres():
    movie_genre_names = MovieGenre.objects.values_list('name', flat=True)
    return movie_genre_names

@register.simple_tag
def get_movie_providers():
    movie_provider_names = MovieProvider.objects.values_list('name', flat=True)
    return movie_provider_names