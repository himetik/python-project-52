from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.statuses.models import Status


class StatusViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.status = Status.objects.create(name='Test Status')

    def test_status_index_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')

    def test_status_create_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('statuses_create'), {'name': 'New Status'}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'statuses_update',
                args=[self.status.pk]),
                {'name': 'Updated Status'},
                follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'statuses_delete',
                args=[self.status.pk]), 
                follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
