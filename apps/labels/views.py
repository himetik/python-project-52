from apps.labels.models import Label
from apps.main.mixins import CustomLoginRequiredMixin
from django.views.generic import ListView, CreateView
from apps.labels.forms import LabelForm
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class LabelIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/labels/labels.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/labels/create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('The label has been successfully created')
