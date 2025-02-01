from django.urls import path
from apps.labels.views import LabelIndexView, LabelCreateView, LabelDeleteView, LabelUpdateView


urlpatterns = [
    path('', LabelIndexView.as_view(), name='labels'),
    path('create/', LabelCreateView.as_view(), name='labels_create'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='labels_delete'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='labels_update')
]
