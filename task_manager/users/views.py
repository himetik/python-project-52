from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from task_manager.main.mixins import UserModificationMixin
from task_manager.users.forms import (
    CustomUserCreationForm, CustomUserChangeForm)


User = get_user_model()


class BaseUserView:
    model = User
    success_url = reverse_lazy('users')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = settings.LOGIN_URL
    success_message = _('The user has been successfully registered')


class UserUpdateView(SuccessMessageMixin, UserModificationMixin, UpdateView):
    template_name = 'users/update.html'
    form_class = CustomUserChangeForm
    success_message = _('The user has been successfully updated')


class UserDeleteView(SuccessMessageMixin, UserModificationMixin, DeleteView):
    template_name = 'users/delete.html'
    success_message = _('The user has been successfully deleted')


class UserIndexView(BaseUserView, ListView):
    template_name = 'users/users.html'
    context_object_name = 'users'
