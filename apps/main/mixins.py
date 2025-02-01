from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


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


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('You are not logged in! Please sign in.'))
        return redirect(reverse('login'))
