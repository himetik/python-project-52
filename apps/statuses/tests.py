from django.test import TestCase
from apps.statuses.models import Status
from apps.main.mixins import SetUpLoggedUserWithStatusMixin
from django.urls import reverse


class StatusIndexViewTest(SetUpLoggedUserWithStatusMixin, TestCase):
    def test_status_index_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

    def test_status_index_view_template(self):
        response = self.client.get(reverse('statuses'))
        self.assertTemplateUsed(response, 'apps/statuses/statuses.html')

    def test_index_page_disallows_non_get_requests(self):
        disallowed_methods = ['post', 'put', 'delete', 'patch']
        url = reverse('statuses')
        for method in disallowed_methods:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 405)

    def test_status_list_view_empty_context(self):
        Status.objects.all().delete()
        response = self.client.get(reverse('statuses'))
        self.assertIn('statuses', response.context)
        self.assertEqual(len(response.context['statuses']), 0)

    def test_status_list_view_context(self):
        Status.objects.create(name="Another Status")
        response = self.client.get(reverse('statuses'))
        self.assertIn('statuses', response.context)
        self.assertGreaterEqual(len(response.context['statuses']), 2)
        self.assertTrue(
            any(
                status.name == "The Status"
                for status in response.context['statuses']
            )
        )
        self.assertTrue(
            any(
                status.name == "Another Status"
                for status in response.context['statuses']
            )
        )


class StatusCreateViewTest(SetUpLoggedUserWithStatusMixin, TestCase):
    def test_status_create_view(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 200)

    def test_status_create_view_template(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertTemplateUsed(response, 'apps/statuses/create.html')

    def test_create_status_success(self):
        data = {'name': 'Status 1'}
        response = self.client.post(reverse('statuses_create'), data)
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='Status 1').exists())


class StatusUpdateViewTest(SetUpLoggedUserWithStatusMixin, TestCase):
    def test_status_update_view(self):
        response = self.client.get(
            reverse('statuses_update', args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_status_update_view_template(self):
        response = self.client.get(
            reverse('statuses_update', args=[self.status.id])
        )
        self.assertTemplateUsed(response, 'apps/statuses/update.html')

    def test_status_update_success(self):
        updated_name = "Updated Status Name"
        response = self.client.post(
            reverse('statuses_update', args=[self.status.id]),
            {'name': updated_name},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, updated_name)


class StatusDeleteViewTest(SetUpLoggedUserWithStatusMixin, TestCase):
    def test_status_delete_view(self):
        response = self.client.get(
            reverse('statuses_delete', args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_status_delete_view_template(self):
        response = self.client.get(
            reverse('statuses_delete', args=[self.status.id])
        )
        self.assertTemplateUsed(response, 'apps/statuses/delete.html')
