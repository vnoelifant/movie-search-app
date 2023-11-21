from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MovieGenre, Movie, MovieProvider, MovieVideo, MovieRecommendation, MovieWatchList


# Register your models here.
admin.site.register(MovieGenre)
admin.site.register(MovieProvider)
admin.site.register(Movie)
admin.site.register(MovieVideo)
admin.site.register(MovieRecommendation)
# Register the CustomUser model with the same options as the default User
admin.site.register(CustomUser, UserAdmin)
admin.site.register(MovieWatchList)
