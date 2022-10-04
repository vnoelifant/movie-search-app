from django.db import models

# Create your models here.
from django.db import models

class Movie(models.Model):
    movie_title = models.CharField(max_length=128)
    
    def __str__(self):
        return self.movie_title