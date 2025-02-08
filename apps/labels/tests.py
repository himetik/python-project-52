from apps.main.mixins import SetUpLoggedUserWithLabelMixin
from django.test import TestCase
from django.urls import reverse


class LabelIndexViewTest(SetUpLoggedUserWithLabelMixin, TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('labels'))
        self.assertTemplateUsed(response, 'apps/labels/labels.html')
        
    def test_view_context(self):
        response = self.client.get(reverse('labels'))
        self.assertTrue('labels' in response.context)
        labels = response.context['labels']
        self.assertIn(self.label, labels)
        label_from_context = labels.first()
        self.assertEqual(label_from_context.id, self.label.id)
        self.assertEqual(str(label_from_context), str(self.label))
        self.assertTrue(hasattr(label_from_context, 'created_at'))
