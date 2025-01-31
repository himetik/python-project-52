from apps.tasks.models import Task
from django_filters.views import FilterView
from apps.main.mixins import CustomLoginRequiredMixin


class TaskIndexView(CustomLoginRequiredMixin, FilterView):
    template_name = 'apps/tasks/tasks.html'
    model = Task
    context_object_name = 'tasks'
