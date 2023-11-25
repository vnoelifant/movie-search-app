from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    MovieGenre,
    Movie,
    MovieProvider,
    MovieVideo,
    MovieRecommendation,
    MovieWatchList,
    TVSeriesGenre,
    TVSeries,
    TVSeriesProvider,
    TVSeriesVideo,
    TVSeriesRecommendation,
    TVSeriesWatchList,
)


# Register your models here.
admin.site.register(MovieGenre)
admin.site.register(MovieProvider)
admin.site.register(Movie)
admin.site.register(MovieVideo)
admin.site.register(MovieRecommendation)
admin.site.register(MovieWatchList)
admin.site.register(TVSeriesGenre)
admin.site.register(TVSeriesProvider)
admin.site.register(TVSeries)
admin.site.register(TVSeriesVideo)
admin.site.register(TVSeriesRecommendation)
admin.site.register(TVSeriesWatchList)
# Register the CustomUser model with the same options as the default User
admin.site.register(CustomUser, UserAdmin)
