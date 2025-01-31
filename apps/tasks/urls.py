from django.urls import path
from apps.tasks.views import TaskIndexView

urlpatterns = [
    path('', TaskIndexView.as_view(), name='tasks'),
]
