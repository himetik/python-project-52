from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from task_manager.main.mixins import CustomLoginRequiredMixin


class BaseStatusView(CustomLoginRequiredMixin):
    model = Status
    success_url = reverse_lazy('statuses')


class StatusIndexView(BaseStatusView, ListView):
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(
    BaseStatusView, SuccessMessageMixin, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_message = _('The status has been successfully created')


class StatusDeleteView(
    BaseStatusView, SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
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
    BaseStatusView, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_message = _("The status has been successfully changed")
