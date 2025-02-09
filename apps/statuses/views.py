from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from apps.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from apps.statuses.forms import StatusForm
from django.urls import reverse_lazy
from apps.main.mixins import CustomLoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect


class StatusIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully created')


class StatusDeleteView(
    CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'apps/statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully deleted')

    def post(self, request, *args, **kwargs):
        status = self.get_object()

        if status.tasks.exists():
            messages.error(
                request, _('Unable to delete a status because it is being used')
            )
            return redirect('statuses')

        return super().post(request, *args, **kwargs)


class StatusUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'apps/statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _("The status has been successfully changed")
