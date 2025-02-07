from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_success_response_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_405_response_code(self):
        DISALLOWERD_METHODS = ['post', 'put', 'delete', 'patch']
        url = reverse('index')
        for method in DISALLOWERD_METHODS:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 405)

    def test_index_correct_template_usage(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')
