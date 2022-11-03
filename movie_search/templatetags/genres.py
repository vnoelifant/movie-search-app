import json
from django import template
from movie_search.models import Genre

register = template.Library()


@register.simple_tag
def get_genres():

    genres = Genre.objects.all()

    print("Genres: ", genres)
    genre_names = [genre.name for genre in genres]
    print("Genre Names", genre_names)
    genre_ids = [genre.id for genre in genres]
    print("Genre IDs", genre_ids)

    return genre_names
