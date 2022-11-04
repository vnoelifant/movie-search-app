import json
from django import template
from movie_search.models import Genre

register = template.Library()


@register.simple_tag
def get_genres():

    genres = Genre.objects.all()
    print("Genres: ", genres)
    genre_names = Genre.objects.values_list('name', flat=True)

    print("Genre Names", genre_names)

    return genre_names
