from django.contrib.auth import get_user_model
from django.views.generic import ListView


class UserIndexView(ListView):
    template_name = 'apps/users/users.html'
    model = get_user_model()
    context_object_name = 'users'
