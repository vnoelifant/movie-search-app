from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    genres = models.TextField(null=True)
    
    def __str__(self):
        return self.genres

