from django.urls import path
from task_manager.users.views import (
    UserIndexView, UserCreateView, UserDeleteView, UserUpdateView)


urlpatterns = [
    path('', UserIndexView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='users_delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='users_update'),
]
