from django.urls import path
from apps.tasks.views import (
    TaskIndexView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskDetailView
)


urlpatterns = [
    path('', TaskIndexView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='tasks_create'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='tasks_delete'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='tasks_update'),
    path('<int:pk>/task/', TaskDetailView.as_view(), name='tasks_instance'),
]
