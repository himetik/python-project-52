from apps.main.mixins import SetUpLoggedUserMixin
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager import settings


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


class UserCreateViewTest(SetUpLoggedUserMixin, TestCase):
    def test_create_user_view_returns_200(self):
        response = self.client.get(reverse('users_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_user_view_uses_correct_template(self):
        response = self.client.get(reverse('users_create'))
        self.assertTemplateUsed(response, 'apps/users/create.html')

    def test_create_user_view_creates_user(self):
        User = get_user_model()
        data = {
            'username': 'test_user',
            'first_name': 'Firstname',
            'last_name': 'LastName',
            'password1': '23977sdv',
            'password2': '23977sdv',
        }
        response = self.client.post(reverse('users_create'), data)
        self.assertRedirects(response, settings.LOGIN_URL)
        self.assertTrue(User.objects.filter(username='test_user').exists())
        user = User.objects.get(username='test_user')
        self.assertEqual(user.first_name, 'Firstname')
        self.assertEqual(user.last_name, 'LastName')
        self.assertTrue(user.check_password('23977sdv'))


class UserUpdateViewTest(SetUpLoggedUserMixin, TestCase):
    def test_update_user_view_returns_200(self):
        response = self.client.get(reverse('users_update', args=(self.user.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_update_user_view_uses_correct_template(self):
        response = self.client.get(reverse('users_update', args=(self.user.pk,)))
        self.assertTemplateUsed(response, 'apps/users/update.html')

    def test_update_user_view_updates_user(self):
        User = get_user_model()
        data = {
            'username': 'new_test_user',
            'first_name': 'NewFirstname',
            'last_name': 'NewLastName',
            'password1': '23977sdv',
            'password2': '23977sdv',
        }
        response = self.client.post(reverse('users_update', args=(self.user.pk,)), data)
        self.assertRedirects(response, reverse('users'))
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, 'new_test_user')
        self.assertEqual(user.first_name, 'NewFirstname')
        self.assertEqual(user.last_name, 'NewLastName')
