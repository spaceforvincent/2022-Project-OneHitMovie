#accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name = 'followers')
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True, upload_to='images/', null=True)
    birthday = models.DateField(blank=True, auto_now=False, null=True)
    blog_url = models.URLField(max_length = 60, blank=True)