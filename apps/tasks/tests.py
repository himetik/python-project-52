from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.tasks.models import Task
from apps.statuses.models import Status

User = get_user_model()

class BaseTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Default Status')
        self.task = Task.objects.create(name='Default Task', description='Default Description', status=self.status, creator=self.user)

class TaskIndexViewTest(BaseTaskTestCase):
    def test_task_list_view_status_code(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_template(self):
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'apps/tasks/tasks.html')

    def test_task_list_view_context(self):
        response = self.client.get(reverse('tasks'))
        self.assertIn('tasks', response.context)
        self.assertIn(self.task, response.context['tasks'])


class TaskCreateViewTest(BaseTaskTestCase):
    def test_create_task_view_status_code(self):
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_task_success(self):
        response = self.client.post(reverse('tasks_create'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': self.status.id
        })
        self.assertEqual(Task.objects.count(), 2)
        self.assertRedirects(response, reverse('tasks'))


class TaskUpdateViewTest(BaseTaskTestCase):
    def test_update_task_view_status_code(self):
        response = self.client.get(reverse('tasks_update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_task_success(self):
        response = self.client.post(reverse('tasks_update', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertRedirects(response, reverse('tasks'))


class TaskDeleteViewTest(BaseTaskTestCase):
    def test_delete_task_view_status_code(self):
        response = self.client.get(reverse('tasks_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_success(self):
        response = self.client.post(reverse('tasks_delete', args=[self.task.id]))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        self.assertRedirects(response, reverse('tasks'))


class TaskSingleViewTest(BaseTaskTestCase):
    def test_task_detail_view_status_code(self):
        response = self.client.get(reverse('tasks_instance', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_template(self):
        response = self.client.get(reverse('tasks_instance', args=[self.task.id]))
        self.assertTemplateUsed(response, 'apps/tasks/task.html')

    def test_task_detail_view_context(self):
        response = self.client.get(reverse('tasks_instance', args=[self.task.id]))
        self.assertIn('task', response.context)
        self.assertEqual(response.context['task'], self.task)
