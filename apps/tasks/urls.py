from django.urls import path
from apps.tasks.views import TaskIndexView, TaskCreateView, TaskDeleteView


urlpatterns = [
    path('', TaskIndexView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='tasks_delete'),
]
