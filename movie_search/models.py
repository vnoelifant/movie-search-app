# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # Add additional fields here if you need
    pass

class Genre(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    genre_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.genre_id}: {self.name}"

    class Meta:
        verbose_name_plural = "genres"


class Provider(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    provider_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.provider_id}: {self.name}"


class Recommendation(models.Model):
    movie_id = models.PositiveSmallIntegerField(default=0)
    poster_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie_id}: {self.poster_path}"

    class Meta:
        verbose_name_plural = "recommendations"


class Movie(models.Model):
    movie_id = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    vote_count = models.PositiveSmallIntegerField(default=0)
    vote_average = models.FloatField(default=0)
    popularity = models.FloatField(default=0, null=True, blank=True)
    release_date = models.CharField(max_length=200, null=True, blank=True)
    runtime = models.IntegerField(default=0, null=True, blank=True)
    production_company = models.CharField(max_length=200, null=True, blank=True)
    overview = models.TextField(default="", null=True, blank=True)
    budget = models.IntegerField(default=0, null=True, blank=True)
    revenue = models.IntegerField(default=0, null=True, blank=True)
    homepage = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.ManyToManyField(
        Recommendation, related_name="movies", blank=True
    )

    def __str__(self):
        return f"{self.movie_id}: {self.title}"


class Video(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.movie_id}: {self.name}, {self.key}"

    class Meta:
        verbose_name_plural = "videos"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name_plural = 'favorites'

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"



