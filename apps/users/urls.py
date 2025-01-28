from django.urls import path
from apps.users.views import UserIndexView


urlpatterns = [
    path('', UserIndexView.as_view(), name='users'),
]
