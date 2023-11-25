import json

from django import template

from movie_search.models import MovieProvider

register = template.Library()

@register.simple_tag
def get_movie_providers():

    movie_providers = MovieProvider.objects.all()
    movie_provider_names = MovieProvider.objects.values_list('name', flat=True)

    return movie_provider_names
