from django.db import models
from django.contrib.auth.models import User

import uuid

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to='profile/', default='profile/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created']

    def __str__(self):
        return str(self.user.username)

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'skills'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name

