from apps.tasks.models import Task
from django_filters.views import FilterView
from apps.main.mixins import CustomLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from apps.tasks.forms import TaskForm
from django.utils.translation import gettext as _
from apps.tasks.filters import TaskFilter
from django.shortcuts import redirect
from django.contrib import messages


class TaskIndexView(CustomLoginRequiredMixin, FilterView):
    template_name = 'apps/tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_filterset(self, filterset_class):
        return filterset_class(self.request.GET, queryset=self.get_queryset(), request=self.request)


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'apps/tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully deleted')

    def check_task_creator(self):
        task = self.get_object()
        if task.creator != self.request.user:
            messages.error(
                self.request,
                _('Only the author of the task can delete it')
            )
            return False
        return True

    def get(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect('tasks')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect('tasks')
        return super().post(request, *args, **kwargs)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'apps/tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully updated')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'apps/tasks/task.html'
    context_object_name = 'task'
