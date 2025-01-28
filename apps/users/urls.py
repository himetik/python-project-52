from django.urls import path
from apps.users.views import UserIndexView, UserCreateView, UserDeleteView


urlpatterns = [
    path('', UserIndexView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='users_delete'),
]
