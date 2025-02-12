from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise forms.ValidationError(_("Label name cannot be empty."))

        return name
