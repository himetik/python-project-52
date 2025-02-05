from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.conf import settings
from apps.users.forms import CustomUserCreationForm
from django.utils.translation import gettext as _
from django.test.utils import override_settings


User = get_user_model()


class BaseUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1', password='password123'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='password123'
        )


@override_settings(LANGUAGE_CODE="en")
class UserListViewTest(BaseUserTestCase):
    def setUp(self):
        self.url = reverse('users')

    def test_user_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'apps/users/users.html')

    def test_user_list_view_context(self):
        response = self.client.get(self.url)
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 2)
        self.assertIn(self.user1, response.context['users'])
        self.assertIn(self.user2, response.context['users'])

    def test_user_list_view_empty(self):
        User.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['users']), 0)


@override_settings(LANGUAGE_CODE="en")
class UserCreateViewTest(BaseUserTestCase):
    def setUp(self):
        self.url = reverse('users_create')
        self.valid_data = {
            'username': 'testuser',
            'password1': 'ComplexPwd123!',
            'password2': 'ComplexPwd123!'
        }

    def test_create_user_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(
            response.context['form'], CustomUserCreationForm
        )

    def test_create_user_success(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, settings.LOGIN_URL)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_create_user_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'WrongPassword123!'
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        form = response.context['form']
        self.assertEqual(
            form.errors['password2'][0],
            "The two password fields didn’t match."
        )

    def test_create_user_duplicate_username(self):
        User.objects.create_user(
            username='testuser',
            password='SomeOtherPwd123!'
        )
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn(
            "A user with that username already exists.",
            form.errors['username']
        )


@override_settings(LANGUAGE_CODE="en")
class UserUpdateViewTest(BaseUserTestCase):
    def setUp(self):
        self.url = reverse('users_update', args=[self.user1.id])
        self.client.login(username='user1', password='password123')

    def test_update_user_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_user_success(self):
        data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'xsw23edc',
            'password2': 'xsw23edc',
        }
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user1.pk}), data
        )
        self.assertRedirects(response, reverse('users'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')

    def test_cannot_update_another_user(self):
        self.client.login(username='user2', password='password123')
        self.client.post(self.url, {'username': 'hacked_user'})
        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.username, 'hacked_user')

    def test_cannot_access_update_view_of_another_user(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


@override_settings(LANGUAGE_CODE="en")
class UserDeleteViewTest(BaseUserTestCase):
    def setUp(self):
        self.url = reverse('users_delete', args=[self.user1.id])
        self.client.login(username='user1', password='password123')

    def test_delete_user_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_success(self):
        self.client.post(self.url)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_cannot_delete_another_user(self):
        self.client.login(username='user2', password='password123')
        self.client.post(self.url)
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())

    def test_cannot_access_delete_view_of_another_user(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


@override_settings(LANGUAGE_CODE="en")
class UserLoginViewTest(BaseUserTestCase):
    def setUp(self):
        self.url = reverse('login')

    def test_login_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            self.url, {'username': 'user1', 'password': 'password123'}
        )
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
            message.message == _('You are logged in')
            for message in messages
            )
        )

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            self.url,
            {'username': 'user1', 'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(response.context['user'].is_authenticated)
