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


class TaskCreateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_create_view(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_template(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertTemplateUsed(response, 'apps/tasks/create.html')

    def test_create_task_success(self):
        data = {
            'name': 'Task 1',
            'status': self.status.id,
            'description': 'Description 1',
        }
        response = self.client.post(reverse('tasks_create'), data)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(
            Task.objects.filter(name='Task 1').exists()
        )


class TaskUpdateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_update_view(self):
        response = self.client.get(
            reverse('tasks_update', args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_template(self):
        response = self.client.get(
            reverse('tasks_update', args=[self.task.pk])
        )
        self.assertTemplateUsed(response, 'apps/tasks/update.html')

    def test_update_task_success(self):
        data = {
            'name': 'Brend new Task Name',
            'status': self.status.id,
        }
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}), data
        )
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Brend new Task Name')
