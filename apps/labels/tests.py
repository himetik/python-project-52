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
