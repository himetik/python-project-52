from django.test import TestCase
from apps.main.mixins import SetUpLoggedUserWithTaskMixin
from django.urls import reverse


class UserLoginViewTest(SetUpLoggedUserWithTaskMixin, TestCase):
    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view_post(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
