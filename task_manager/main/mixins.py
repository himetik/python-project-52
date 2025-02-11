from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, UpdateView


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


class DeleteMixin(SuccessMessageMixin, DeleteView):
    success_message = _('The object has been successfully deleted')

    def test_func(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not authorized to perform this action.')
        )
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return self.success_url


class UpdateMixin(SuccessMessageMixin, UpdateView):
    success_message = _("The object has been successfully updated")

    def test_func(self) -> bool:
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You are not authorized to perform this action.")
        )
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return self.success_url
