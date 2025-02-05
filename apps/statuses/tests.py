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

    def get_response(
            self, 
            view_name,
            args=None,
            method='get',
            data=None,
            follow=False
        ):
        url = reverse(view_name, args=args)
        return getattr(self.client, method)(url, data, follow=follow)


class StatusIndexViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Test Status')

    def test_status_list_view(self):
        response = self.get_response('statuses')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/statuses/statuses.html')
        self.assertIn('statuses', response.context)
        self.assertIn(self.status, response.context['statuses'])


class StatusCreateViewTest(BaseStatusTestCase):
    def test_create_status(self):
        response = self.get_response(
            'statuses_create',
            method='post',
            data={'name': 'New Status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())


class StatusUpdateViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Old Status')

    def test_update_status(self):
        response = self.get_response(
            'statuses_update',
            args=[self.status.id],
            method='post',
            data={'name': 'Updated Status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')


class StatusDeleteViewTest(BaseStatusTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='Delete Status')

    def test_delete_status(self):
        response = self.get_response(
            'statuses_delete',
            args=[self.status.id],
            method='post', 
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_delete_status_with_tasks(self):
        Task.objects.create(
            name='Test Task',
            status=self.status,
            creator=self.user
        )
        response = self.get_response(
            'statuses_delete',
            args=[self.status.id],
            method='post',
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())

    def test_delete_nonexistent_status(self):
        response = self.get_response(
            'statuses_delete',
            args=[99999],
            method='post',
            follow=True
        )

        self.assertEqual(response.status_code, 404)
