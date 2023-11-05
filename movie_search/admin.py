from django.contrib import admin 

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Genre, Movie, Provider, Video, Recommendation, Favorite


# Register your models here.
admin.site.register(Genre)
admin.site.register(Provider)
admin.site.register(Movie)
admin.site.register(Video)
admin.site.register(Recommendation)
# Register the CustomUser model with the same options as the default User
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Favorite)
