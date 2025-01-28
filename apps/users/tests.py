from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.conf import settings
from apps.users.forms import CustomUserCreationForm
from django.utils.translation import gettext as _



User = get_user_model()


class SetUpLoggedUserMixin:
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        login_successful = self.client.login(
            username='testuser',
            password='password123'
        )
        if not login_successful:
            raise Exception("Failed to log in test user")
        super().setUp() if hasattr(super(), 'setUp') else None


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


class UserCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('users_create')
        self.valid_data = {
            'username': 'testuser',
            'password1': 'ComplexPwd123!',
            'password2': 'ComplexPwd123!',
        }
        self.invalid_data = {
            'username': '',
            'password1': 'pwd',
            'password2': 'pwd123',
        }

    def test_get_request_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/users/create.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_post_valid_data_creates_user_and_redirects(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, settings.LOGIN_URL)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            message.message == 'The user has been successfully registered' and message.level == messages[0].level
            for message in messages
        ))

    def test_post_invalid_data_does_not_create_user_and_shows_errors(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/users/create.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('password2', form.errors)

    def test_form_fields_presence(self):
        response = self.client.get(self.url)
        form = response.context['form']
        expected_fields = ['username', 'password1', 'password2']
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_success_message_present_on_successful_registration(self):
        response = self.client.post(self.url, data=self.valid_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            message.message == 'The user has been successfully registered'
            for message in messages
        ))


class UserDeleteViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.url = reverse('users_delete', args=[self.user1.id])

    def test_user_can_delete_self(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.url, follow=True)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
        self.assertRedirects(response, reverse('users'))
        messages = list(response.context['messages'])
        self.assertTrue(any(message.message == 'The user has been successfully deleted' for message in messages))

    def test_user_cannot_delete_another_user(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(self.url, follow=True)
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertRedirects(response, reverse('users'))
        messages = list(response.context['messages'])
        self.assertTrue(any(message.message == 'You are not authorized to modify another user.' for message in messages))


class UserUpdateViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.url = reverse('users_update', args=[self.user1.id])
        self.valid_data = {
            'username': 'updated_user1',
        }

    def test_user_can_update_own_profile(self):
        self.client.login(username='user1', password='password123')
        self.client.post(self.url, data=self.valid_data)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updated_user1')

    def test_user_cannot_update_another_user_profile(self):
        self.client.login(username='user2', password='password123')
        self.client.post(self.url, data=self.valid_data)
        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.username, 'updated_user1')


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )

    def test_login_view_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_with_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), _('You are logged in'))

    def test_login_with_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertFalse(response.context['user'].is_authenticated)


class UserLogoutViewTest(SetUpLoggedUserMixin, TestCase):
    def test_logout_view_status_code(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_success(self):
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
        response = self.client.get(reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), _('You are logged out'))
