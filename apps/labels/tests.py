from apps.main.mixins import SetUpLoggedUserWithLabelMixin
from django.test import TestCase
from django.urls import reverse
from apps.labels.models import Label
from django.contrib.messages import get_messages
from django.utils.translation import gettext as _
from apps.tasks.models import Task, Status


class LabelIndexViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_labels_page_is_accessible(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        
    def test_labels_page_uses_correct_template(self):
        response = self.client.get(reverse('labels'))
        self.assertTemplateUsed(response, 'apps/labels/labels.html')
        
    def test_labels_page_context_contains_labels(self):
        response = self.client.get(reverse('labels'))
        self.assertTrue('labels' in response.context)
        labels = response.context['labels']
        self.assertIn(self.label, labels)
        label_from_context = labels.first()
        self.assertEqual(label_from_context.id, self.label.id)
        self.assertEqual(str(label_from_context), str(self.label))
        self.assertTrue(hasattr(label_from_context, 'created_at'))

    def test_labels_page_displays_empty_list_when_no_labels(self):
        self.label.delete()
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['labels']), 0)

    def test_labels_page_displays_specific_label_name(self):
        response = self.client.get(reverse('labels'))
        self.assertContains(response, "The Label")


class LabelCreateViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_create_label_page_is_accessible(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_label_page_uses_correct_template(self):
        response = self.client.get(reverse('labels_create'))
        self.assertTemplateUsed(response, 'apps/labels/create.html')

    def test_create_label_success(self):
        data = {'name': 'Unique Label'}
        response = self.client.post(reverse('labels_create'), data, follow=True)
        self.assertTrue(Label.objects.filter(name='Unique Label').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(msg) == _('The label has been successfully created')
                for msg in messages
            )
        )
        self.assertRedirects(response, reverse('labels'))

    def test_create_label_with_existing_name_fails(self):
        existing_label = Label.objects.create(name="Duplicate Label")
        data = {"name": existing_label.name}
        response = self.client.post(reverse("labels_create"), data)
        self.assertEqual(
            Label.objects.filter(name="Duplicate Label").count(), 1
        )
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Label с таким Имя уже существует."), form.errors["name"]
        )

    def test_create_label_with_empty_name_fails(self):
        initial_label_count = Label.objects.count()
        data = {"name": ""}
        response = self.client.post(reverse("labels_create"), data)
        self.assertEqual(Label.objects.count(), initial_label_count)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Обязательное поле."), form.errors["name"]
        )

    def test_create_label_with_whitespace_name(self):
        Label.objects.create(name="Same Label")
        data = {"name": "  Same Label  "}
        response = self.client.post(reverse("labels_create"), data)
        self.assertEqual(Label.objects.filter(name="Same Label").count(), 1)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Label с таким Имя уже существует."), form.errors["name"]
        )

    def test_create_label_exceeding_max_length_fails(self):
        max_length = Label._meta.get_field("name").max_length
        too_long_name = "L" * (max_length + 1)
        data = {"name": too_long_name}
        response = self.client.post(reverse("labels_create"), data)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _(
                "Убедитесь, что это значение содержит не более {} символов "
                "(сейчас {}).".format(max_length, max_length + 1)
            ),
            form.errors["name"],
        )


class LabelDeleteVewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_delete_label_page_is_accessible(self):
        response = self.client.get(
            reverse('labels_delete', kwargs={'pk': self.label.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_label_page_uses_correct_template(self):
        response = self.client.get(
            reverse('labels_delete', kwargs={'pk': self.label.id})
        )
        self.assertTemplateUsed(response, 'apps/labels/delete.html')

    def test_delete_label_success(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.id}), follow=True
        )
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(msg) == _('The label has been successfully deleted')
                for msg in messages
            )
        )
        self.assertRedirects(response, reverse('labels'))

    def test_delete_label_with_tasks(self):
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            status=self.status, 
            creator=self.user, 
            executor=self.user,
        )
        self.task.labels.add(self.label)

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk})
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]),
            _('Невозможно удалить метку, потому что она используется')
        )

    def test_delete_label_with_non_existing_id_fails(self):
        non_existing_id = self.label.id + 999
        response = self.client.post(
            reverse(
                'labels_delete',
                kwargs={'pk': non_existing_id}), follow=True
        )
        self.assertEqual(response.status_code, 404)


class LabelUpdateViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_update_label_page_is_accessible(self):
        response = self.client.get(
            reverse('labels_update', kwargs={'pk': self.label.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_label_page_uses_correct_template(self):
        response = self.client.get(
            reverse('labels_update', kwargs={'pk': self.label.id})
        )
        self.assertTemplateUsed(response, 'apps/labels/update.html')

    def test_update_label_success(self):
        updated_data = {'name': 'Updated Label'}
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.id}),
            updated_data,
            follow=True
        )
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(msg) == _('The label has been successfully changed')
                for msg in messages
            )
        )
        self.assertRedirects(response, reverse('labels'))

    def test_update_label_with_non_existing_id_fails(self):
        non_existing_id = self.label.id + 919
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': non_existing_id}),
            {'name': 'New Name'},
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_update_label_with_existing_name_fails(self):
        existing_label = Label.objects.create(name="Duplicate Label")
        data = {"name": existing_label.name}
        response = self.client.post(
            reverse("labels_update", kwargs={"pk": self.label.id}),
            data,
        )
        self.label.refresh_from_db()
        self.assertNotEqual(self.label.name, existing_label.name)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Label с таким Имя уже существует."), form.errors["name"]
        )

    def test_update_label_with_empty_name_fails(self):
        data = {"name": ""}
        response = self.client.post(
            reverse("labels_update", kwargs={"pk": self.label.id}),
            data,
        )
        self.label.refresh_from_db()
        self.assertNotEqual(self.label.name, "")
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Обязательное поле."), form.errors["name"]
        )

    def test_update_label_with_whitespace_name(self):
        Label.objects.create(name="Duplicate Label")
        data = {"name": "  Duplicate Label  "}
        response = self.client.post(
            reverse("labels_update", kwargs={"pk": self.label.id}),
            data,
        )
        self.label.refresh_from_db()
        self.assertNotEqual(self.label.name, "Duplicate Label")
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _("Label с таким Имя уже существует."), form.errors["name"]
        )

    def test_update_label_exceeding_max_length_fails(self):
        max_length = Label._meta.get_field("name").max_length
        too_long_name = "L" * (max_length + 1)
        data = {"name": too_long_name}
        response = self.client.post(
            reverse("labels_update", kwargs={"pk": self.label.id}),
            data,
        )
        self.label.refresh_from_db()
        self.assertNotEqual(self.label.name, too_long_name)
        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn(
            _(
                "Убедитесь, что это значение содержит не более {} символов "
                "(сейчас {}).".format(max_length, max_length + 1)
            ),
            form.errors["name"],
        )
