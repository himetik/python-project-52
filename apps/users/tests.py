from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.user1 = cls.user_model.objects.create_user(username='testuser1', password='password123')
        cls.user2 = cls.user_model.objects.create_user(username='testuser2', password='password123')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users'))
        self.assertTemplateUsed(response, 'apps/users/users.html')

    def test_view_returns_all_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, response.context['users'])
        self.assertIn(self.user2, response.context['users'])
        self.assertEqual(len(response.context['users']), 2)
