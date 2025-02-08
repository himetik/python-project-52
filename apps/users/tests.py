from apps.main.mixins import SetUpLoggedUserMixin
from django.test import TestCase
from django.urls import reverse


class UserIndexViewTest(SetUpLoggedUserMixin, TestCase):
    def test_users_view_returns_200(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_users_view_uses_correct_template(self):
        response = self.client.get(reverse('users'))
        self.assertTemplateUsed(response, 'apps/users/users.html')

    def test_users_view_contains_single_user(self):
        response = self.client.get(reverse('users'))
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 1)
        self.assertEqual(response.context['users'][0], self.user)

    def test_users_view_empty_when_no_users(self):
        self.user.delete()
        response = self.client.get(reverse('users'))
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 0)
