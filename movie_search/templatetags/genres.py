from django import template
from movie_search import media_api

register = template.Library()

@register.simple_tag
def get_genres():
    # Get a dictionary of available genres
    genres = media_api.get_genres("/genre/movie/list")
    return genres