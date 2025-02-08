from django.test import TestCase
from apps.statuses.models import Status # noqa
from apps.main.mixins import SetUpLoggedUserWithStatusMixin
from django.urls import reverse


class StatusIndexViewTest(SetUpLoggedUserWithStatusMixin, TestCase):
    def test_status_index_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)

    def test_status_index_view_template(self):
        response = self.client.get(reverse('statuses'))
        self.assertTemplateUsed(response, 'apps/statuses/statuses.html')
