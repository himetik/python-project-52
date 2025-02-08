from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_page_loads_successfully(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_page_disallows_non_get_requests(self):
        disallowed_methods = ['post', 'put', 'delete', 'patch']
        url = reverse('index')
        for method in disallowed_methods:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 405)


class ErrorPagesTest(TestCase):
    def test_404_page_loads_for_nonexistent_url(self):
        response = self.client.get('/unreachable/')
        self.assertEqual(response.status_code, 404)

    def test_404_page_uses_correct_template(self):
        response = self.client.get('/unreachable/')
        self.assertTemplateUsed(response, '404.html')
