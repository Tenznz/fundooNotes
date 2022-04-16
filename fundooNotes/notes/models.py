from django.db import models
from datetime import datetime
from user.models import User


class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    color = models.CharField(max_length=50, default="")
    archive = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

