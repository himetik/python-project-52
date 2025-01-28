from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from apps.users.forms import CustomUserCreationForm
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL
    success_message = _('You are logged in')


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'apps/users/create.html'
    form_class = CustomUserCreationForm
    success_url = settings.LOGIN_URL
    success_message = _('The user has been successfully registered')


class UserIndexView(ListView):
    template_name = 'apps/users/users.html'
    model = get_user_model()
    context_object_name = 'users'
