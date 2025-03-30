import os
from uuid import uuid4
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{slugify(instance.username)}_{uuid4().hex[:8]}.{ext}"
    return os.path.join('profile_pics', filename)

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)
    short_bio = models.TextField(blank=True)
    is_writer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
