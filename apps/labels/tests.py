from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.labels.models import Label


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
