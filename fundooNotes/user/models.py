from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    age = models.IntegerField()
    phone = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    

# class LoginData(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.PROTECT)
#     token = models.CharField(max_length=200)
#     created_at = models.DateTimeField(default=datetime.now, blank=True)
