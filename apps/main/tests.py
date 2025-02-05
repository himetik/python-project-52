from django.urls import reverse
from django.test import TestCase


class Get404ViewTest(TestCase):
    def test_get_404_renders_correct_template(self):
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class IndexViewTest(TestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
