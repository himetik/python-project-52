from django.views.generic import TemplateView
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'index.html'


def get_404(request, exception):
    return render(request, '404.html', status=404)
