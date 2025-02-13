from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task, Status
from task_manager.users.tests import SetUpLoggedUserMixin
from task_manager.labels.models import Label
from task_manager.tests import constants


class SetUpLoggedUserWithLabelMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.main_label = Label.objects.create(name=constants.MAIN_LABEL)


class LabelIndexViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_labels_page_is_accessible(self):
        url = reverse('labels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_labels_page_uses_correct_template(self):
        url = reverse('labels')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'labels/labels.html')

    def test_labels_page_context_contains_labels(self):
        url = reverse('labels')
        response = self.client.get(url)
        self.assertTrue('labels' in response.context)
        labels = response.context['labels']
        self.assertIn(self.main_label, labels)
        label_from_context = labels.first()
        self.assertEqual(label_from_context.id, self.main_label.id)
        self.assertEqual(str(label_from_context), str(self.main_label))
        self.assertTrue(hasattr(label_from_context, 'created_at'))

    def test_labels_page_displays_empty_list_when_no_labels(self):
        self.main_label.delete()
        url = reverse('labels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['labels']), 0)

    def test_labels_page_displays_specific_label_name(self):
        url = reverse('labels')
        response = self.client.get(url)
        self.assertContains(response, self.main_label.name)


class LabelCreateViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_create_label_page_is_accessible(self):
        url = reverse('labels_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_label_page_uses_correct_template(self):
        url = reverse('labels_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'labels/create.html')

    def test_create_label_success(self):
        url = reverse("labels_create")
        response = self.client.post(
            url,
            {"name": constants.LABEL_NAME_1},
            follow=True
        )

        self.assertTrue(
            Label.objects.filter(name=constants.LABEL_NAME_1).exists()
        )

        messages = list(get_messages(response.wsgi_request))
        success_message = _("The label has been successfully created")
        self.assertTrue(
            any(str(msg) == success_message for msg in messages)
        )

        self.assertRedirects(response, reverse("labels"))

    def test_create_label_with_existing_name_fails(self):
        url = reverse("labels_create")
        self.client.post(
            url,
            {"name": constants.LABEL_NAME_1},
            follow=True
        )

        response = self.client.post(
            url,
            {"name": constants.LABEL_NAME_1},
            follow=False
        )

        self.assertEqual(
            Label.objects.filter(name=constants.LABEL_NAME_1).count(), 
            1
        )

        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertGreater(len(form.errors["name"]), 0)

    def test_create_label_with_empty_name_fails(self):
        initial_label_count = Label.objects.count()
        url = reverse("labels_create")
        response = self.client.post(url, {"name": constants.EMPTY_NAME})
        self.assertEqual(Label.objects.count(), initial_label_count)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertTrue(len(form.errors["name"]) > 0)

    def test_create_label_with_whitespace_name(self):
        Label.objects.create(name=constants.LABEL_NAME_3)
        url = reverse("labels_create")
        response = self.client.post(
            url,
            {"name": constants.WHITESPACED_LABEL_NAME_3}
        )
        self.assertEqual(
            Label.objects.filter(
                name=constants.LABEL_NAME_3).count(),
                1
            )
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertTrue(len(form.errors["name"]) > 0)

    def test_create_label_exceeding_max_length_fails(self):
        url = reverse("labels_create")
        response = self.client.post(
            url,
            {"name": constants.LONG_LABEL}
        )
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertTrue(len(form.errors["name"]) > 0)


class LabelDeleteVewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_delete_label_page_is_accessible(self):
        url = reverse("labels_delete", kwargs={"pk": self.main_label.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_label_page_uses_correct_template(self):
        url = reverse("labels_delete", kwargs={"pk": self.main_label.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "labels/delete.html")

    def test_delete_label_success(self):
        url = reverse("labels_delete", kwargs={"pk": self.main_label.id})
        response = self.client.post(url, follow=True)
        self.assertFalse(Label.objects.filter(id=self.main_label.id).exists())
        messages = list(get_messages(response.wsgi_request))
        success_message = _("The label has been successfully deleted")
        self.assertTrue(any(str(msg) == success_message for msg in messages))
        self.assertRedirects(response, reverse("labels"))

    def test_delete_label_with_tasks(self):
        status = Status.objects.create(name=constants.STATUS_NAME_1)
        task = Task.objects.create(
            name=constants.TASK_NAME_1,
            status=status,
            creator=self.user,
            executor=self.user,
        )

        task.labels.add(self.main_label)
        url = reverse("labels_delete", kwargs={"pk": self.main_label.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("labels"))
        self.assertTrue(Label.objects.filter(pk=self.main_label.pk).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            _("Unable to delete a label because it is being used")
        )

    def test_delete_label_with_non_existing_id_fails(self):
        non_existing_id = self.main_label.id + 999
        url = reverse("labels_delete", kwargs={"pk": non_existing_id})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 404)


class LabelUpdateViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_update_label_page_is_accessible(self):
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_label_page_uses_correct_template(self):
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "labels/update.html")

    def test_update_label_success(self):
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.post(
            url,
            {"name": constants.LABEL_NAME_2},
            follow=True
        )
        self.main_label.refresh_from_db()
        self.assertEqual(self.main_label.name, constants.LABEL_NAME_2)
        messages = list(get_messages(response.wsgi_request))
        success_message = _("The label has been successfully changed")
        self.assertTrue(any(str(msg) == success_message for msg in messages))
        self.assertRedirects(response, reverse("labels"))

    def test_update_label_with_non_existing_id_fails(self):
        non_existing_id = self.main_label.id + 919
        url = reverse("labels_update", kwargs={"pk": non_existing_id})
        response = self.client.post(
            url,
            {"name": constants.LABEL_NAME_4},
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_update_label_with_existing_name_fails(self):
        existing_label = Label.objects.create(name=constants.LABEL_NAME_1)
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.post(url, {"name": existing_label.name})
        self.main_label.refresh_from_db()
        self.assertNotEqual(self.main_label.name, existing_label.name)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertGreater(len(form.errors["name"]), 0)

    def test_update_label_with_empty_name_fails(self):
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.post(url, {"name": constants.EMPTY_NAME})
        self.main_label.refresh_from_db()
        self.assertNotEqual(self.main_label.name, constants.EMPTY_NAME)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(_("This field is required."), form.errors["name"])

    def test_update_label_with_whitespace_name(self):
        Label.objects.create(name=constants.LABEL_NAME_1)
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.post(url, name=constants.LABEL_NAME_1)
        self.main_label.refresh_from_db()
        self.assertNotEqual(self.main_label.name, constants.LABEL_NAME_1)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertGreater(len(form.errors["name"]), 0)

    def test_update_label_exceeding_max_length_fails(self):
        url = reverse("labels_update", kwargs={"pk": self.main_label.id})
        response = self.client.post(url, {"name": constants.LONG_LABEL})
        self.main_label.refresh_from_db()
        self.assertNotEqual(self.main_label.name, constants.LONG_LABEL)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertGreater(len(form.errors["name"]), 0)
