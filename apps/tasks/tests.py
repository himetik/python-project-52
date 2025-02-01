from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.tasks.models import Task
from apps.statuses.models import Status
from django.urls import reverse


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


class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        self.status = Status.objects.create(name='New')
        self.create_url = reverse('tasks_create')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_get_create_view_as_logged_in_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/tasks/create.html')

    def test_create_task_successfully(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.create_url, {
            'name': 'New Task',
            'description': 'Task description',
            'status': self.status.id
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.creator, self.user)
        self.assertEqual(task.status, self.status)
        self.assertContains(response, 'The task has been successfully created')

    def test_create_task_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.create_url, {}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.exists())


class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123')
        self.other_user = get_user_model().objects.create_user(
            username='otheruser', password='password456')
        self.status = Status.objects.create(name='New')
        self.task = Task.objects.create(
            name='Test Task',
            description='Task description',
            status=self.status,
            creator=self.user
        )
        self.delete_url = reverse('tasks_delete', args=[self.task.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_delete_task_successfully(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        self.assertContains(response, 'The task has been successfully deleted')

    def test_delete_task_by_non_creator_fails(self):
        self.client.login(username='otheruser', password='password456')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())


class TaskUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123')
        self.other_user = get_user_model().objects.create_user(
            username='otheruser', password='password456')
        self.status = Status.objects.create(name='New')
        self.task = Task.objects.create(
            name='Test Task',
            description='Task description',
            status=self.status,
            creator=self.user
        )
        self.update_url = reverse('tasks_update', args=[self.task.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_update_task_successfully(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.update_url, {
            'name': 'Updated Task',
            'description': 'Updated description',
            'status': self.status.id
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated description')
        self.assertContains(response, 'The task has been successfully updated')


class TaskDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.executor = get_user_model().objects.create_user(username="executor", password="password123")
        self.status = Status.objects.create(name="In Progress")
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            creator=self.user,
            executor=self.executor,
            created_at=timezone.now()
        )
        self.url = reverse("tasks_instance", kwargs={"pk": self.task.pk})

    def test_task_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "apps/tasks/task.html")

    def test_task_detail_view_context(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["task"], self.task)
        self.assertEqual(response.context["task"].name, "Test Task")
        self.assertEqual(response.context["task"].description, "Test Description")
        self.assertEqual(response.context["task"].status, self.status)
        self.assertEqual(response.context["task"].creator, self.user)
        self.assertEqual(response.context["task"].executor, self.executor)

    def test_task_detail_view_nonexistent_task(self):
        url = reverse("tasks_instance", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
