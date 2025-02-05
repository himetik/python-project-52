from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from apps.labels.models import Label
from apps.tasks.models import Task
from apps.statuses.models import Status


User = get_user_model()


@override_settings(LANGUAGE_CODE="en")
class LabelIndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.label = Label.objects.create(name='Test Label')
        self.client.login(username='testuser', password='testpass')

    def test_label_list_view_status_code(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)

    def test_label_list_view_template(self):
        response = self.client.get(reverse('labels'))
        self.assertTemplateUsed(response, 'apps/labels/labels.html')

    def test_label_list_view_context(self):
        response = self.client.get(reverse('labels'))
        self.assertIn('labels', response.context)
        self.assertIn(self.label, response.context['labels'])


@override_settings(LANGUAGE_CODE="en")
class LabelCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_create_label_view_status_code(self):
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_label_form(self):
        self.client.post(reverse('labels_create'), {'name': 'New Label'})
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.first().name, 'New Label')

    def test_create_label_success(self):
        response = self.client.post(
            reverse('labels_create'), {'name': 'Another Label'}, follow=True
        )
        self.assertIn(
            'The label has been successfully created', response.content.decode()
        )

    def test_create_view_redirects_if_not_logged_in(self):
        create_url = reverse("labels_create")
        self.client.logout()
        response = self.client.get(create_url)
        self.assertTrue(
            response.url == reverse("login") or response.url.startswith(
                f"{reverse('login')}?next="
            ),
            f"Unexpected redirect URL: {response.url}"
        )


@override_settings(LANGUAGE_CODE="en")
class LabelUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.label = Label.objects.create(name='Old Label')
        self.client.login(username='testuser', password='testpass')

    def test_update_label_view_status_code(self):
        response = self.client.get(
            reverse('labels_update', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_update_label_success(self):
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}),
            {'name': 'Updated Label'}, follow=True
        )
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')
        self.assertIn(
            'The label has been successfully changed', response.content.decode()
        )


@override_settings(LANGUAGE_CODE="en")
class LabelDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.label = Label.objects.create(name='Deletable Label')
        self.client.login(username='testuser', password='testpass')

    def test_delete_label_view_status_code(self):
        response = self.client.get(
            reverse('labels_delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_label_success(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}), follow=True
        )
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assertIn(
            'The label has been successfully deleted', response.content.decode()
        )

    def test_delete_label_with_tasks(self):
        status = Status.objects.create(name='New')
        task = Task.objects.create(
            name='Test Task', creator=self.user, status=status
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}), follow=True
        )
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertIn(
            'Cannot delete the label because it is currently in use',
            response.content.decode()
        )
