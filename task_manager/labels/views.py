from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.labels.models import Label
from task_manager.main.mixins import CustomLoginRequiredMixin
from task_manager.labels.forms import LabelForm


class BaseLabelClass(CustomLoginRequiredMixin):
    model = Label
    success_url = reverse_lazy('labels')


class LabelIndexView(BaseLabelClass, ListView):
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelCreateView(
    BaseLabelClass, SuccessMessageMixin, CreateView):
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_message = _('The label has been successfully created')


class LabelDeleteView(
    BaseLabelClass, SuccessMessageMixin, DeleteView):
    template_name = 'labels/delete.html'
    success_message = _('The label has been successfully deleted')

    def post(self, request, *args, **kwargs):
        label = self.get_object()

        if label.tasks.exists():
            messages.error(
                request, _('Unable to delete a label because it is being used')
            )
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)


class LabelUpdateView(
    BaseLabelClass, SuccessMessageMixin, UpdateView):
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_message = _('The label has been successfully changed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Edit Label')
        return context
