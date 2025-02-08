from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(_('name'), max_length=180, unique=True, blank=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    def __str__(self):
        return self.name
