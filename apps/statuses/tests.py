from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from apps.statuses.models import Status
from apps.tasks.models import Task


User = get_user_model()


@override_settings(LANGUAGE_CODE="en")
class BaseStatusTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def setUp(self):
        self.client.login(username='testuser', password='testpass')


@override_settings(LANGUAGE_CODE="en")
class StatusIndexViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Test Status')

    def test_status_list_view_status_code(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

    def test_status_list_view_template(self):
        response = self.client.get(reverse('statuses'))
        self.assertTemplateUsed(response, 'apps/statuses/statuses.html')

    def test_status_list_view_context(self):
        response = self.client.get(reverse('statuses'))
        self.assertIn('statuses', response.context)
        self.assertIn(self.status, response.context['statuses'])


@override_settings(LANGUAGE_CODE="en")
class StatusCreateViewTest(BaseStatusTestCase):
    def test_create_status_view_status_code(self):
        response = self.client.get(reverse('statuses_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_status_success(self):
        response = self.client.post(
            reverse('statuses_create'), {'name': 'New Status'}, follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())


@override_settings(LANGUAGE_CODE="en")
class StatusUpdateViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Old Status')

    def test_update_status_success(self):
        response = self.client.post(
            reverse(
                'statuses_update',
                args=[self.status.id]),
                {'name': 'Updated Status'},
                follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')


@override_settings(LANGUAGE_CODE="en")
class StatusDeleteViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Delete Status')

    def test_delete_status_success(self):
        response = self.client.post(
            reverse('statuses_delete', args=[self.status.id]), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_delete_status_with_tasks(self):
        Task.objects.create(
            name='Test Task', status=self.status, creator=self.user
        )
        response = self.client.post(
            reverse('statuses_delete', args=[self.status.id]), follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())
