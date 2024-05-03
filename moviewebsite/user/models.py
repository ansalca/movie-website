from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

# Define the Movie model
class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    youtube_trailer_link = models.URLField()

    def __str__(self):
        return self.title


# Define the Category model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('user:category', args=[self.name])


