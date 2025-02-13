from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.main.mixins import (
    CustomLoginRequiredMixin, TaskCreatorCheckMixin)


class BaseTaskView(CustomLoginRequiredMixin):
    model = Task
    success_url = reverse_lazy('tasks')


class TaskIndexView(BaseTaskView, FilterView):
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(BaseTaskView, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskDeleteView(
    BaseTaskView, TaskCreatorCheckMixin,
    SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    success_message = _('The task has been successfully deleted')


class TaskUpdateView(BaseTaskView, SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_message = _('The task has been successfully updated')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
