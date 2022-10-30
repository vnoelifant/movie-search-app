import datetime
from django import template

register = template.Library()

@register.simple_tag
def get_years():

    year_dropdown = []
    for year in range((datetime.datetime.now().year + 2), 1940, -1):
        year_dropdown.append(year)

    return year_dropdown