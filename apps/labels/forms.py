from django.forms import ModelForm
from apps.labels.models import Label


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = [
            'name',
        ]
