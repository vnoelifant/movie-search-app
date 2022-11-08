from datetime import date

from django import template

register = template.Library()


@register.filter
def year_range_desc(start_year):
    next_year = date.today().year + 1
    return range(next_year, start_year - 1, -1)
