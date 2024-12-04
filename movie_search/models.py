# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    # Add additional fields here if you need
    pass


class MovieGenre(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    genre_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.genre_id}: {self.name}"

    class Meta:
        verbose_name_plural = "movie genres"


class MovieRecommendation(models.Model):
    movie_id = models.PositiveIntegerField(default=0, unique=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie_id}: {self.poster_path}"

    class Meta:
        verbose_name_plural = "movie recommendations"


class MovieProductionCompany(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    production_company_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.production_company_id}: {self.name}"

    class Meta:
        verbose_name_plural = "movie production companies"


class Movie(models.Model):
    movie_id = models.PositiveIntegerField(default=0, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField(MovieGenre, related_name="movies", blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    vote_count = models.PositiveIntegerField(default=0)
    vote_average = models.FloatField(default=0)
    popularity = models.FloatField(default=0, null=True, blank=True)
    release_date = models.CharField(max_length=200, null=True, blank=True)
    runtime = models.IntegerField(default=0, null=True, blank=True)
    production_companies = models.ManyToManyField(
        MovieProductionCompany, related_name="movies", blank=True
    )
    overview = models.TextField(default="", null=True, blank=True)
    budget = models.IntegerField(default=0, null=True, blank=True)
    revenue = models.IntegerField(default=0, null=True, blank=True)
    homepage = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.ManyToManyField(
        MovieRecommendation, related_name="movies", blank=True
    )

    def __str__(self):
        return f"{self.movie_id}: {self.title}"


class MovieProvider(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    provider_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.provider_id}: {self.name}"


class MovieVideo(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.movie_id}: {self.name}, {self.key}"

    class Meta:
        verbose_name_plural = "movie videos"


class MovieWatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "movie")
        verbose_name_plural = "movie watchlist"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class TVSeriesGenre(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    genre_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.genre_id}: {self.name}"

    class Meta:
        verbose_name_plural = "tv series genres"


class TVSeriesRecommendation(models.Model):
    series_id = models.PositiveIntegerField(default=0, unique=True)
    poster_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.series_id}: {self.poster_path}"

    class Meta:
        verbose_name_plural = "tv series recommendations"


class TVSeriesProductionCompany(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    production_company_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.production_company_id}: {self.name}"

    class Meta:
        verbose_name_plural = "tv series production companies"


class TVSeries(models.Model):
    series_id = models.PositiveIntegerField(default=0, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)
    genres = models.ManyToManyField(TVSeriesGenre, related_name="tvseries", blank=True)
    tagline = models.CharField(max_length=200, null=True, blank=True)
    vote_count = models.PositiveIntegerField(default=0)
    vote_average = models.FloatField(default=0)
    popularity = models.FloatField(default=0, null=True, blank=True)
    first_air_date = models.CharField(max_length=200, null=True, blank=True)
    number_of_episodes = models.IntegerField(default=0, null=True, blank=True)
    number_of_seasons = models.IntegerField(default=0, null=True, blank=True)
    production_companies = models.ManyToManyField(
        TVSeriesProductionCompany, related_name="tvseries", blank=True
    )
    overview = models.TextField(default="", null=True, blank=True)
    homepage = models.CharField(max_length=200, null=True, blank=True)
    recommendation = models.ManyToManyField(
        TVSeriesRecommendation, related_name="tvseries", blank=True
    )

    def __str__(self):
        return f"{self.series_id}: {self.name}"


class TVSeriesProvider(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    provider_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.provider_id}: {self.name}"


class TVSeriesVideo(models.Model):
    tvseries = models.ForeignKey(
        TVSeries, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.tvseries.series_id}: {self.name}, {self.key}"

    class Meta:
        verbose_name_plural = "tv series videos"


class TVSeriesWatchList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tvseries = models.ForeignKey(TVSeries, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "tvseries")
        verbose_name_plural = "tv series watchlist"

    def __str__(self):
        return f"{self.user.username} - {self.tvseries.name}"
