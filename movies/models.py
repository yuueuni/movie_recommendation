from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=20)
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100, blank=True)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
