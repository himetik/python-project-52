from task_manager.tasks.models import Task
from django_filters.views import FilterView
from task_manager.main.mixins import CustomLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.forms import TaskForm
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.filters import TaskFilter
from django.shortcuts import redirect
from django.contrib import messages


class TaskIndexView(CustomLoginRequiredMixin, FilterView):
    template_name = 'tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_filterset(self, filterset_class):
        return filterset_class(
            data=self.request.GET,
            queryset=self.get_queryset(),
            request=self.request,
        )


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully deleted')

    def check_task_creator(self) -> bool:
        task = self.get_object()
        user = self.request.user

        if task.creator != user:
            messages.error(
                self.request, _('Only the author of the task can delete it')
            )
            return False

        return True

    def get(self, request, *args, **kwargs):
        if self.check_task_creator():
            return super().get(request, *args, **kwargs)
        return redirect("tasks")

    def post(self, request, *args, **kwargs):
        if self.check_task_creator():
            return super().post(request, *args, **kwargs)
        return redirect("tasks")


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('The task has been successfully updated')


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
