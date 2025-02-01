from apps.tasks.models import Task
from django_filters.views import FilterView
from apps.main.mixins import CustomLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from apps.tasks.forms import TaskForm
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from apps.tasks.filters import TaskFilter


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.creator != self.request.user:
            raise PermissionDenied(_('Only the author of the task can delete it'))
        return obj


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
