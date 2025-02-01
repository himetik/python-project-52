from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.tasks.models import Task
from apps.statuses.models import Status

class TaskIndexViewTests(TestCase):
    def setUp(self):
        self.creator = get_user_model().objects.create_user(
            username='creator',
            password='creator123'
        )
        self.executor = get_user_model().objects.create_user(
            username='executor',
            password='executor123'
        )
        self.status = Status.objects.create(
            name='In Progress'
        )
        self.task1 = Task.objects.create(
            name='Test Task 1',
            description='Description for task 1',
            status=self.status,
            creator=self.creator,
            executor=self.executor,
            created_at=timezone.now()
        )
        self.task2 = Task.objects.create(
            name='Test Task 2',
            description='Description for task 2',
            status=self.status,
            creator=self.creator,
            executor=None,
            created_at=timezone.now()
        )
        self.client = Client()
        self.tasks_url = '/tasks/'

    def test_login_required(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_view_with_logged_in_user(self):
        self.client.login(username='creator', password='creator123')
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/tasks/tasks.html')
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        task1 = tasks.get(name='Test Task 1')
        self.assertEqual(task1.creator, self.creator)
        self.assertEqual(task1.executor, self.executor)
        self.assertEqual(task1.status, self.status)
        task2 = tasks.get(name='Test Task 2')
        self.assertEqual(task2.creator, self.creator)
        self.assertIsNone(task2.executor)
        self.assertEqual(task2.status, self.status)

    def test_task_unique_name(self):
        with self.assertRaises(Exception):
            Task.objects.create(
                name='Test Task 1',
                description='Another description',
                status=self.status,
                creator=self.creator
            )

    def test_filter_by_status(self):
        self.client.login(username='creator', password='creator123')
        new_status = Status.objects.create(name='Completed')
        Task.objects.create(
            name='Test Task 3',
            status=new_status,
            creator=self.creator
        )
        response = self.client.get(f"{self.tasks_url}?status={self.status.id}")
        self.assertEqual(response.context['tasks'].count(), 2)
        response = self.client.get(f"{self.tasks_url}?status={new_status.id}")
        self.assertEqual(response.context['tasks'].count(), 1)

    def test_filter_by_executor(self):
        self.client.login(username='creator', password='creator123')
        response = self.client.get(f"{self.tasks_url}?executor={self.executor.id}")
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertEqual(response.context['tasks'].first(), self.task1)
        response = self.client.get(f"{self.tasks_url}?executor=")
        tasks = response.context['tasks']
        self.assertTrue(any(task.executor is None for task in tasks))

    def test_task_str_method(self):
        self.assertEqual(str(self.task1), 'Test Task 1')
