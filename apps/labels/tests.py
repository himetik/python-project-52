from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.labels.models import Label
from django.contrib.messages import get_messages
from apps.tasks.models import Task 
from apps.statuses.models import Status


class LabelIndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.label1 = Label.objects.create(name="Label 1")
        self.label2 = Label.objects.create(name="Label 2")

    def test_view_url_accessible_by_logged_in_user(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("labels"))
        self.assertTemplateUsed(response, "apps/labels/labels.html")

    def test_context_contains_labels(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("labels"))
        labels = response.context["labels"]
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0].name, "Label 1")
        self.assertEqual(labels[1].name, "Label 2")


class LabelCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.create_url = reverse("labels_create")

    def test_create_view_accessible_by_logged_in_user(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        expected_url = reverse("login")
        self.assertTrue(response.url.startswith(expected_url), f"Unexpected redirect URL: {response.url}")

    def test_create_view_uses_correct_template(self):
        response = self.client.get(self.create_url)
        self.assertTemplateUsed(response, "apps/labels/create.html")

    def test_create_label_successfully(self):
        response = self.client.post(self.create_url, {"name": "New Label"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name="New Label").exists())

    def test_create_label_with_empty_name_fails(self):
        response = self.client.post(self.create_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        form = response.context.get("form")
        self.assertIsNotNone(form, "Form was not passed into the template context")
        self.assertTrue(form.errors, "Form contains no errors")
        self.assertIn("name", form.errors, "Field 'name' did not trigger an error")
        self.assertEqual(Label.objects.count(), 0)


class LabelDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.label = Label.objects.create(name="Test Label")
        self.client.login(username="testuser", password="password")

    def test_delete_label_success(self):
        response = self.client.post(reverse("labels_delete", kwargs={"pk": self.label.pk}))
        self.assertRedirects(response, reverse("labels"))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_delete_label_in_use_fails(self):
        self.client.login(username="testuser", password="password")
        status = Status.objects.create(name="New")
        task = Task.objects.create(name="Test Task", creator=self.user, status=status)
        task.labels.add(self.label)
        response = self.client.post(reverse("labels_delete", kwargs={"pk": self.label.pk}))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertEqual(str(messages[0]), "Cannot delete the label because it is currently in use")
        self.assertRedirects(response, reverse("labels"))

    def test_delete_label_requires_login(self):
        self.client.logout()
        response = self.client.post(reverse("labels_delete", kwargs={"pk": self.label.pk}))
        self.assertNotEqual(response.status_code, 200)
