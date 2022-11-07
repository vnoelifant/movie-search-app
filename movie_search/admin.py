from django.contrib import admin
from movie_search.models import Genre, Provider

# Register your models here.
admin.site.register(Genre)
admin.site.register(Provider)