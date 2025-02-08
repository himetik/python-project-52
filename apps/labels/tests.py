from apps.main.mixins import SetUpLoggedUserWithLabelMixin
from django.test import TestCase
from django.urls import reverse


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
