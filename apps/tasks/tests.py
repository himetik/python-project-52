from django.test import TestCase
from apps.main.mixins import SetUpLoggedUserWithTaskMixin
from django.urls import reverse
from apps.tasks.models import Task


class TaskIndexViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_status_index_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_status_index_view_template(self):
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'apps/tasks/tasks.html')

    def test_task_list_view_empty_context(self):
        Task.objects.all().delete()
        response = self.client.get(reverse('tasks'))
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 0)

    def test_task_list_view_context(self):
        response = self.client.get(reverse('tasks'))
        self.assertIn('tasks', response.context)
        self.assertGreaterEqual(len(response.context['tasks']), 1)
        self.assertTrue(
            any(
                task.name == "The Task"
                for task in response.context['tasks']
            )
        )
