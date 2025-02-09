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
        url = reverse("tasks")
        response = self.client.get(url)
        self.assertIn("tasks", response.context)
        tasks = response.context["tasks"]
        self.assertGreaterEqual(len(tasks), 1)
        self.assertTrue(any(task.name == "The Task" for task in tasks))


class TaskCreateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_create_view(self):
        url = reverse("tasks_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_template(self):
        url = reverse("tasks_create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "apps/tasks/create.html")

    def test_create_task_success(self):
        url = reverse("tasks_create")
        data = {
            "name": "Task 1",
            "status": self.status.id,
            "description": "Description 1",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks"))
        self.assertTrue(Task.objects.filter(name="Task 1").exists())

    def test_create_task_max_length_exceeded(self):
        url = reverse("tasks_create")
        long_name = "A" * (self.task._meta.get_field("name").max_length + 1)
        data = {
            "name": long_name,
            "status": self.status.id,
            "description": "Description 1",
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.assertFalse(Task.objects.filter(name=long_name).exists())

    def test_create_task_empty_name(self):
        url = reverse("tasks_create")
        data = {
            "name": "",
            "status": self.status.id,
            "description": "Test description",
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.assertFalse(Task.objects.filter(name="").exists())


class TaskUpdateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_update_view(self):
        url = reverse("tasks_update", args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_update_view_template(self):
        url = reverse("tasks_update", args=[self.task.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "apps/tasks/update.html")

    def test_update_task_success(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        data = {
            "name": "Brand new Task Name",
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Brand new Task Name")

    def test_task_name_max_length_exceeded(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        long_name = "A" * (self.task._meta.get_field("name").max_length + 1) 
        data = {
            "name": long_name,
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, long_name)

    def test_update_task_empty_name(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        data = {
            "name": "",
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, "")


class TaskDeleteViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_delete_view(self):
        url = reverse("tasks_delete", args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_task_success(self):
        url = reverse("tasks_delete", args=[self.task.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
