from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Movie(models.Model) :
    title = models.CharField(max_length=100)
    released_date = models.DateField(null=True, blank=True)
    adult = models.BooleanField(null=True, blank=True)
    vote_avg = models.FloatField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

    def __str__(self):
        return self.title

class MovieComment(models.Model):
    STAR_CHOICES = [
        ('5',"★★★★★"),
        ('4',"★★★★"),
        ('3',"★★★"),
        ('2',"★★"),
        ('1',"★"),
        (None, '선택')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    rating = models.CharField(max_length=10, choices=STAR_CHOICES)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)