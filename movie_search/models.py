from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200)
    genre_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.tmdb_id}: {self.name}"

    class Meta:
        verbose_name_plural = "genres"

class Provider(models.Model):
    name = models.CharField(max_length=200)
    provider_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.provider_id}: {self.name}"


class Movie(models.Model):
    movie_id = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    vote_count = models.PositiveSmallIntegerField(default=0)
    vote_average = models.PositiveSmallIntegerField(default=0)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    release_date = models.CharField(max_length=200, null=True, blank=True)
    runtime = models.IntegerField(default=0, null=True, blank=True)
    production_company = models.CharField(max_length=200, null=True, blank=True)
    overview = models.TextField(default="", null=True, blank=True)
    budget = models.IntegerField(default=0, null=True, blank=True)
    revenue = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    homepage = models.CharField(max_length=200, null=True, blank=True)
    video = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.tmdb_id}: {self.title}"