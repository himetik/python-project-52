from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import (
    CustomUserCreationForm, CustomUserChangeForm)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from task_manager.main.mixins import DeleteMixin, UpdateMixin


User = get_user_model()


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL
    success_message = _('You are logged in')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = settings.LOGIN_URL
    success_message = _('The user has been successfully registered')


class UserDeleteView(DeleteMixin, UserPassesTestMixin):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('The user has been successfully deleted')

    def test_func(self):
        return self.request.user == self.get_object()

    def get_redirect_url(self):
        return reverse_lazy('users')


class UserUpdateView(UpdateMixin, UserPassesTestMixin):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = _('The user has been successfully updated')

    def test_func(self):
        return self.request.user == self.get_object()

    def get_redirect_url(self):
        return reverse_lazy("users")


class UserIndexView(ListView):
    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'
