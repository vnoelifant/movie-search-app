from django.contrib import admin

from movie_search.models import Genre, Movie, Provider, Video

# Register your models here.
admin.site.register(Genre)
admin.site.register(Provider)
admin.site.register(Movie)
admin.site.register(Video)