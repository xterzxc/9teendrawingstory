from django.views.generic import TemplateView
from draw.models import Drawing

from .utils import CF_ACCESS

class IndexView(TemplateView):
    template_name = "base/index.html"
    def get_context_data(self, **kwargs):
        cf_access = CF_ACCESS()
        cf_delete, status_code = cf_access.delete('canvas-image(5).png')
        print(status_code)
        if status_code == 204:
            print('DELETED')
        context = super().get_context_data(**kwargs)
        context['images'] = Drawing.objects.all()
        return context