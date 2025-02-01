from django.urls import path
from apps.labels.views import LabelIndexView


urlpatterns = [
    path('', LabelIndexView.as_view(), name='labels'),
]
