from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.statuses.models import Status
from apps.labels.models import Label


class Task(models.Model):
    name = models.CharField(_('name'), max_length=256, unique=True)
    description = models.TextField(_('description'), blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name=_('status'),
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_('creator'),
        related_name='creator_tasks',
    )
    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('executor'),
        related_name='executor_tasks',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('labels'),
        related_name='tasks',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('created at')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
