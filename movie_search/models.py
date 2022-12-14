from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200)
    tmdb_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.tmdb_id}: {self.name}"

class Provider(models.Model):
    name = models.CharField(max_length=200)
    provider_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.provider_id}: {self.name}"
