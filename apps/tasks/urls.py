from django.urls import path
from apps.tasks.views import TaskIndexView, TaskCreateView


urlpatterns = [
    path('', TaskIndexView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
]
