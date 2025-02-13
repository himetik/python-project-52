from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from task_manager.users.models import User


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not logged in! Please sign in.')
        )
        return redirect(reverse('login'))


class UserModificationMixin(UserPassesTestMixin):
    model = User
    success_url = reverse_lazy('users')
    
    def test_func(self) -> bool:
        return self.request.user == self.get_object()
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not authorized to modify another user.')
        )
        return redirect('users')


class TaskCreatorCheckMixin:
    def check_task_creator(self) -> bool:
        task = self.get_object()
        if task.creator != self.request.user:
            messages.error(
                self.request,
                _('Only the author of the task can delete it')
            )
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect(self.get_failure_url())
        return super().dispatch(request, *args, **kwargs)

    def get_failure_url(self):
        return reverse_lazy('tasks')
