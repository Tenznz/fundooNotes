from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField()
    phone = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
