from apps.labels.models import Label
from apps.main.mixins import CustomLoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from apps.labels.forms import LabelForm
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect


class LabelIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/labels/labels.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/labels/create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('The label has been successfully created')


class LabelDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'apps/labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('The label has been successfully deleted')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(request, _('Cannot delete the label because it is currently in use'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
