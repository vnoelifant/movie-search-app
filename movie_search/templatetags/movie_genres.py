import json

from django import template

from movie_search.models import MovieGenre

register = template.Library()


@register.simple_tag
def get_movie_genres():

    movie_genres = MovieGenre.objects.all()
    movie_genre_names = MovieGenre.objects.values_list('name', flat=True)
    
    return movie_genre_names
