from django.utils import timezone
from django.db import models


class Status(models.Model):
    name = models.CharField(('name'), max_length=200, unique=True)
    created_at = models.DateTimeField(('created at'), default=timezone.now)

    def __str__(self):
        return self.name
