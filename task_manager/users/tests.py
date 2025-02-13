from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils.translation import gettext as _
from task_manager import settings
from task_manager.tests import constants


User = get_user_model()


class SetUpLoggedUserMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'username': constants.MAIN_USER["username"],
            'password': constants.MAIN_USER["password1"]
        }
        cls.user = get_user_model().objects.create_user(**cls.user_data)

    def setUp(self):
        super().setUp()
        self.client.login(**self.user_data)


class UserIndexViewTest(SetUpLoggedUserMixin, TestCase):
    view_url = reverse('users')

    def test_users_view_returns_200(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_users_view_uses_correct_template(self):
        response = self.client.get(self.view_url)
        self.assertTemplateUsed(response, 'users/users.html')

    def test_users_view_contains_single_user(self):
        response = self.client.get(self.view_url)
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 1)
        self.assertEqual(response.context['users'][0], self.user)

    def test_users_view_empty_when_no_users(self):
        self.user.delete()
        response = self.client.get(self.view_url)
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 0)

    def test_users_sorted_by_id_desc(self):
        User.objects.create(username=constants.USER_1["username"])
        User.objects.create(username=constants.USER_2["username"])
        response = self.client.get(self.view_url)
        self.assertIn('users', response.context)
        users = list(response.context['users'])
        sorted_users = sorted(users, key=lambda u: u.id, reverse=True)
        self.assertEqual(users, sorted_users)


class UserCreateViewTest(TestCase):
    creation_url = reverse('users_create')

    def test_create_user_view_returns_200(self):
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_view_uses_correct_template(self):
        response = self.client.get(self.creation_url)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_create_user_view_creates_user(self):
        response = self.client.post(self.creation_url, constants.USER_1)
        self.assertRedirects(response, settings.LOGIN_URL)
        self.assertTrue(User.objects.filter(username='user_1').exists())
        user = User.objects.get(username=constants.USER_1['username'])
        self.assertEqual(user.first_name, constants.USER_1['first_name'])
        self.assertEqual(user.last_name, constants.USER_1['last_name'])
        self.assertTrue(user.check_password(constants.USER_1['password1']))

    def test_create_user_fails_if_passwords_dont_match(self):
        invalid_data = constants.USER_1.copy()
        invalid_data["password2"] = constants.WRONG_PASS
        response = self.client.post(self.creation_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username=constants.USER_1['username']).exists()
        )
        form = response.context['form']
        self.assertIn('password2', form.errors)
        self.assertEqual(
            form.errors['password2'][0],
            _("The two password fields didn't match.")
        )


class UserUpdateViewTest(SetUpLoggedUserMixin, TestCase):
    def test_update_user_view_returns_200(self):
        url = reverse("users_update", args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_user_view_uses_correct_template(self):
        url = reverse("users_update", args=[self.user.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/update.html")

    def test_user_update_view_changes_user_data(self):
        url = reverse("users_update", args=[self.user.pk])
        response = self.client.post(url, constants.USER_2)
        self.assertRedirects(response, reverse("users"))
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, constants.USER_2["username"])
        self.assertEqual(user.first_name, constants.USER_2["first_name"])
        self.assertEqual(user.last_name, constants.USER_2["last_name"])

    def test_update_nonexistent_user_returns_404(self):
        nonexistent_user_id = self.user.pk
        self.user.delete()
        url = reverse("users_update", args=[nonexistent_user_id])
        response = self.client.post(url, constants.USER_2)
        self.assertEqual(response.status_code, 404)


class UserDeleteViewTest(SetUpLoggedUserMixin, TestCase):
    def test_delete_user_view_returns_200(self):
        url = reverse("users_delete", args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_view_uses_correct_template(self):
        url = reverse("users_delete", args=[self.user.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "users/delete.html")

    def test_delete_user_view_deletes_user(self):
        url = reverse("users_delete", args=[self.user.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users"))
        self.assertFalse(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )

    def test_delete_nonexistent_user_returns_404(self):
        nonexistent_user_id = self.user.pk
        self.user.delete()
        url = reverse("users_delete", args=[nonexistent_user_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class UserLoginViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username=constants.USER_1["username"],
            password=constants.USER_1["password1"]
        )
        self.login_url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': constants.USER_1["username"],
            'password': constants.USER_1["password1"]
        })
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(m) == _('You are logged in') for m in messages))

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': constants.USER_1["username"],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.non_field_errors())

    def test_login_page_loads_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_page_uses_correct_template(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'login.html')


class UserLogoutViewTest(SetUpLoggedUserMixin, TestCase):
    logout_url = reverse('logout')

    def test_logout_view_status_code(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_success(self):
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), _('You are logged out'))
