from django.forms import CheckboxInput
from django_filters import filters, FilterSet
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    own_tasks = filters.BooleanFilter(
        field_name='creator',
        method='filter_own_tasks',
        label=_('Only your tasks'),
        widget=CheckboxInput()
    )

    status = filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status')
    )

    executor = filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(), 
        label=_('Executor')
    )

    labels = filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    class Meta:
        model = Task

        fields = [
            'own_tasks',
            'status',
            'executor',
            'labels'
        ]

    def filter_own_tasks(self, queryset, name, value):
        if value and getattr(self, "request", None):
            return queryset.filter(creator=self.request.user)
        return queryset
