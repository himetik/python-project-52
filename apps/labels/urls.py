from django.urls import path
from apps.labels.views import LabelIndexView, LabelCreateView


urlpatterns = [
    path('', LabelIndexView.as_view(), name='labels'),
    path('create/', LabelCreateView.as_view(), name='labels_create'),
]
