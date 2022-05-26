from tkinter import CASCADE
from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.

class Advertisement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'advertisements')
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='advertisements')
    title = models.CharField(max_length=100)
    picture = models.ImageField(blank=True, upload_to='images/', null=True)
    website = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_advertisements')

class AdvertisementComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advertisement_comments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='advertisement_comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)