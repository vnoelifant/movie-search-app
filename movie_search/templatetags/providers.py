import json
from django import template
from movie_search.models import Provider

register = template.Library()

@register.simple_tag
def get_providers():

    providers = Provider.objects.all()
    print("Providers: ", providers)
    provider_names = Provider.objects.values_list('name', flat=True)

    print("Provider Names", provider_names)

    return provider_names
