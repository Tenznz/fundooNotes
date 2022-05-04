from django.db import models
from datetime import datetime

from user.models import User


class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
