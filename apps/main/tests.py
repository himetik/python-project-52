from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_success_response_code(self):
        response = self.response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_correct_template_usage(self):
        response = self.response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_disallowed_methods(self):
        disallowed_methods = ['post', 'put', 'delete', 'patch']
        url = reverse('index')
        for method in disallowed_methods:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 405)


class ErrorsPagesTest(TestCase):
    def test_get_404(self):
        response = self.response = self.client.get('/unreachable/')
        self.assertEqual(response.status_code, 404)
    
    def test_get_404_template_usage(self):
        response = self.response = self.client.get('/unreachable/')
        self.assertTemplateUsed(response, '404.html')
