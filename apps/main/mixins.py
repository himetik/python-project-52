from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from apps.labels.models import Label
from apps.statuses.models import Status
from apps.tasks.models import Task


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request, _('You are not logged in! Please sign in.')
        )
        return redirect(reverse('login'))


class SetUpLoggedUserMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username': 'testuser', 'password': 'testpassword'}
        cls.user = get_user_model().objects.create_user(**cls.user_data)

    def setUp(self):
        super().setUp()
        self.client.login(**self.user_data)


class SetUpLoggedUserWithLabelMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.label = Label.objects.create(name='The Label')


class SetUpLoggedUserWithStatusMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='The Status')


class SetUpLoggedUserWithTaskMixin(SetUpLoggedUserMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.status = Status.objects.create(name='The Status')
        cls.task = Task.objects.create(
            name='The Task', status=cls.status, creator=cls.user
        )
