from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.tests import SetUpLoggedUserMixin
from task_manager.tests import constants 



class SetUpLoggedUserWithTaskMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name=constants.MAIN_STATUS)
        cls.task = Task.objects.create(
            name=constants.MAIN_TASK,
            status=cls.status,
            creator=cls.user
        )


class TaskIndexViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    task_view_url = reverse('tasks')

    def test_status_index_view(self):
        response = self.client.get(self.task_view_url)
        self.assertEqual(response.status_code, 200)

    def test_status_index_view_template(self):
        response = self.client.get(self.task_view_url)
        self.assertTemplateUsed(response, 'tasks/tasks.html')

    def test_task_list_view_empty_context(self):
        Task.objects.all().delete()
        response = self.client.get(self.task_view_url)
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 0)

    def test_task_list_view_context(self):
        response = self.client.get(self.task_view_url)
        self.assertIn("tasks", response.context)
        tasks = response.context["tasks"]
        self.assertGreaterEqual(len(tasks), 1)
        self.assertTrue(any(task.name == constants.MAIN_TASK for task in tasks))


class TaskCreateViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    creation_url = reverse("tasks_create")

    def test_task_create_view(self):
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 200)

    def test_task_create_view_template(self):
        response = self.client.get(self.creation_url)
        self.assertTemplateUsed(response, "tasks/create.html")

    def test_create_task_success(self):
        data = {
            "name": constants.TASK_NAME_1,
            "status": self.status.id,
            "description": constants.TASK_DESCRIPTION,
        }
        response = self.client.post(self.creation_url, data)
        self.assertRedirects(response, reverse("tasks"))
        self.assertTrue(
            Task.objects.filter(name=constants.TASK_NAME_1).exists()
        )

    def test_create_task_max_length_exceeded(self):
        data = {
            "name": constants.LONG_TASK,
            "status": self.status.id,
            "description": constants.TASK_DESCRIPTION,
        }
        response = self.client.post(self.creation_url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.assertFalse(Task.objects.filter(name=constants.LONG_TASK).exists())

    def test_create_task_empty_name(self):
        data = {
            "name": constants.EMPTY_NAME,
            "status": self.status.id,
            "description": constants.TASK_DESCRIPTION,
        }
        response = self.client.post(self.creation_url, data)
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
        self.assertTemplateUsed(response, "tasks/update.html")

    def test_update_task_success(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        data = {
            "name": constants.TASK_NAME_2,
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("tasks"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, constants.TASK_NAME_2)

    def test_task_name_max_length_exceeded(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        data = {
            "name": constants.LONG_TASK,
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, constants.LONG_TASK)

    def test_update_task_empty_name(self):
        url = reverse("tasks_update", kwargs={"pk": self.task.pk})
        data = {
            "name": constants.EMPTY_NAME,
            "status": self.status.id,
        }
        response = self.client.post(url, data)
        self.assertTrue("name" in response.context["form"].errors)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, constants.EMPTY_NAME)


class TaskDeleteViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_task_delete_view(self):
        url = reverse("tasks_delete", args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_delete_used_correct_tamplate(self):
        url = reverse("tasks_delete", args=[self.task.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "tasks/delete.html")

    def test_delete_task_success(self):
        url = reverse("tasks_delete", args=[self.task.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
