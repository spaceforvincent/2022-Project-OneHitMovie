#accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CHOICES=[('1', '일반 회원'),('0','판매 회원')]

    followings = models.ManyToManyField("self", symmetrical=False, related_name = 'followers')
    isgeneral = models.CharField(max_length=10, choices=CHOICES)
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True, upload_to='images/', null=True)
    birthday = models.DateField(blank=True, auto_now=False, null=True)
    blog_url = models.URLField(max_length = 300, blank=True, null=True)