from django.db import models

from user.models import User


class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
