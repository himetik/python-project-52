from django.forms import ModelForm
from apps.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
        ]
