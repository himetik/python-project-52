from django.urls import path
from apps.statuses.views import (StatusIndexView)


urlpatterns = [
    path('', StatusIndexView.as_view(), name='statuses'),
]
