from apps.main.mixins import SetUpLoggedUserMixin
from django.test import TestCase
from django.urls import reverse


class UserIndexViewTest(SetUpLoggedUserMixin, TestCase):
    def test_(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test__(self):
        response = self.client.get(reverse('users'))
        self.assertTemplateUsed(response, 'apps/users/users.html')

    def test___(self):
        response = self.client.get(reverse('users'))
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 1)
        self.assertEqual(response.context['users'][0], self.user)

    def test____(self):
        self.user.delete()
        response = self.client.get(reverse('users'))
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 0)
