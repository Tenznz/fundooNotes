from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    age = models.IntegerField()
    phone = models.CharField(max_length=10)
