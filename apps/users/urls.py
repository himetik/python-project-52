from django.urls import path
from apps.users.views import UserIndexView, UserCreateView


urlpatterns = [
    path('', UserIndexView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='users_create'),
]
