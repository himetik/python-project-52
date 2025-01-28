from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from apps.users.forms import CustomUserCreationForm
from django.conf import settings
from django.utils.translation import gettext as _


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'apps/users/create.html'
    form_class = CustomUserCreationForm
    success_url = settings.LOGIN_URL
    success_message = _('The user has been successfully registered')


class UserIndexView(ListView):
    template_name = 'apps/users/users.html'
    model = get_user_model()
    context_object_name = 'users'
