import datetime
from django import template

register = template.Library()

@register.simple_tag
def get_years():

    year_dropdown = []
    for year in range(1940, (datetime.datetime.now().year + 2)):
        year_dropdown.append(year)
    year_dropdown.reverse()

    return year_dropdown