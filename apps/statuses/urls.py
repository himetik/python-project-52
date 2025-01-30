from django.urls import path
from apps.statuses.views import StatusIndexView, StatusCreateView


urlpatterns = [
    path('', StatusIndexView.as_view(), name='statuses'),
    path('create/', StatusCreateView.as_view(), name='statuses_create'),
]
