from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView
from apps.statuses.models import Status
from django.contrib.messages.views import SuccessMessageMixin
from apps.statuses.forms import StatusForm
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _('You are not logged in! Please sign in.'))
        return redirect(reverse('login'))


class StatusIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully created')
