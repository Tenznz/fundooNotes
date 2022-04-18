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

    def get_format(self):
        return {
            "title": self.title,
            "description": self.description
        }

    def __str__(self):
        return self.title


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    note = models.ManyToManyField(Note)

    def __str__(self):
        return self.name
