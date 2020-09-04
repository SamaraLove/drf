from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Profile(models.Model):
    rating = models.IntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # profile_img = models.ImageField(upload_to='avatars/', null=True, blank=True)
    profile_img = models.URLField(default = "", max_length=400)
    bio = models.TextField(default = "", max_length=500, blank=True)
    location = models.CharField(default = "", max_length=30, blank=True)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="userprofile"
    )