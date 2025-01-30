from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    def __str__(self):
        return self.name
