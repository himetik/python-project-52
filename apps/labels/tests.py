from apps.main.mixins import SetUpLoggedUserWithLabelMixin
from django.test import TestCase
from django.urls import reverse
from apps.labels.models import Label
from django.contrib.messages import get_messages
from django.utils.translation import gettext as _


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
