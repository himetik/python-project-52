from django.forms import ModelForm
from apps.statuses.models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
