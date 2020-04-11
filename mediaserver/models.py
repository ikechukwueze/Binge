from django.db import models
from django.core.files.storage import FileSystemStorage
from Binge.settings import MOVIE_STORAGE_ROOT, MOVIE_STORAGE_URL

fs = FileSystemStorage(MOVIE_STORAGE_ROOT, MOVIE_STORAGE_URL)
# Create your models here.

class mediaDatabase(models.Model):
    title               = models.CharField(max_length=150)
    year                = models.IntegerField()
    release_date        = models.DateField()
    rated               = models.CharField(max_length=10)
    runtime             = models.DurationField()
    genre               = models.CharField(max_length=300)
    #genre_2            = models.CharField(max_length=100)
    #genre_3            = models.CharField(max_length=100)
    director            = models.CharField(max_length=255)
    writers             = models.TextField()
    cast                = models.TextField()
    plot                = models.TextField()
    poster              = models.ImageField(upload_to='movie_posters/')
    backdrop            = models.ImageField(upload_to='movie_posters/')
    ratings_imdb        = models.FloatField()
    ratings_metacritic  = models.FloatField()
    ratings_rotten      = models.FloatField()
    ratings_average     = models.FloatField()
    date_added          = models.DateTimeField(auto_now=True)
    favourite           = models.BooleanField(default=False)
    movie_path          = models.CharField(max_length=400, blank=True)
    movie_url           = models.CharField(max_length=400, blank=True)



    def __str__(self):
        return self.title