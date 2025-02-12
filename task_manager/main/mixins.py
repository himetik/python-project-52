from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request, _('You are not logged in! Please sign in.')
        )
        return redirect(reverse('login'))


class BaseActionMixin(SuccessMessageMixin):
    success_message = ""

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


class UserDeleteMixin(BaseActionMixin, DeleteView):
    success_message = _('The object has been successfully deleted')


class UserUpdateMixin(BaseActionMixin, UpdateView):
    success_message = _("The object has been successfully updated")


class TaskCreatorCheckMixin:
    def check_task_creator(self) -> bool:
        task = self.get_object()
        if task.creator != self.request.user:
            messages.error(
                self.request, _('Only the author of the task can delete it')
            )
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect(self.get_failure_url())
        return super().dispatch(request, *args, **kwargs)

    def get_failure_url(self):
        return reverse_lazy('tasks')
