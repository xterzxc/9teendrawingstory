from django.views.generic import TemplateView
from draw.models import Drawing
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import CF_ACCESS

class IndexView(TemplateView):
    template_name = "base/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        drawings = Drawing.objects.all()
        paginator = Paginator(drawings, 6)
        page_obj = paginator.get_page(1)
        context['images'] = page_obj
        context['has_next'] = page_obj.has_next()
        
        return context

class LoadDrawingsView(TemplateView):
    def get(self, request):
        page_number = request.GET.get('page')
        drawings = Drawing.objects.all()
        
        paginator = Paginator(drawings, 6)
        page_obj = paginator.get_page(page_number)

        data = []
        for drawing in page_obj:
            data.append({
                'imglink': drawing.imglink,
                'title': drawing.title,
                'avatarlink': drawing.owner.avatarlink
            })
        
        return JsonResponse({
            'data': data,
            'has_next': page_obj.has_next()
        })