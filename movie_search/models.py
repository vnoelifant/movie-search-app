from django.db import models

# Create your models here.
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=200)
    id =  models.AutoField(primary_key=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.name}"

