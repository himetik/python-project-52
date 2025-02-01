from apps.tasks.models import Task
from django_filters.views import FilterView
from apps.main.mixins import CustomLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.tasks.forms import TaskForm
from django.utils.translation import gettext as _


class TaskIndexView(CustomLoginRequiredMixin, FilterView):
    template_name = 'apps/tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
