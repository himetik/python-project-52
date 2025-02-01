from apps.labels.models import Label
from apps.main.mixins import CustomLoginRequiredMixin
from django.views.generic import ListView


class LabelIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/labels/labels.html'
    model = Label
    context_object_name = 'labels'
