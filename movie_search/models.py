from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(null=True)
    id =   models.IntegerField(null=True)
    
    def __str__(self):
        return self.name

