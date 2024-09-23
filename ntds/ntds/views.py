from django.views.generic import TemplateView
from draw.models import Drawing


class IndexView(TemplateView):
    template_name = "base/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Drawing.objects.all()
        return context