import os
from uuid import uuid4
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db import models

# Define custom path and filename for user profile pictures
# Format: profile_<slug_username>_<uniqueid>.ext

def user_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_{slugify(instance.username)}_{uuid4().hex[:8]}.{ext}"
    return os.path.join('profile_pics', filename)

# Extend Django's AbstractUser to add custom fields
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)

    # Gender choices for the gender field
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # Selectable gender field
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)  # Optional profile image
    short_bio = models.TextField(blank=True)  # Optional short biography
    is_writer = models.BooleanField(default=False)  # Whether the user can publish content/articles

    def __str__(self):
        return self.username  # Display username in admin and shell
