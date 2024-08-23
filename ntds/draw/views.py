import requests
import uuid
from requests_aws4auth import AWS4Auth
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Drawing
from django.http import JsonResponse
from ntds.settings import CF_UPLOAD_URL, CF_GET_URL, CF_SECRET_ACCESS_KEY, CF_ACCESS_KEY, CF_REGION, CF_SERVICE

def DrawingView(request):
    return render(request, 'draw/draw.html')

class DrawingCreateView(CreateView):
    http_method_names = ['post']
    model = Drawing
    fields = ['title', 'description']

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        image.name = str(uuid.uuid4())


        url = CF_UPLOAD_URL + image.name
        authorization = AWS4Auth(CF_ACCESS_KEY, CF_SECRET_ACCESS_KEY, CF_REGION, CF_SERVICE)
        
        
        put_headers = {
            'Content-Type': image.content_type,
        }

        try:
            response = requests.put(
                url,
                data=image,
                headers=put_headers,
                auth=authorization,
            )
            if response.status_code != 200:
                return JsonResponse({'error': 'Failed to upload image'}, status=500)
        except requests.RequestException as e:
            return JsonResponse({'error': 'Error while uploading image'}, status=500)




        self.object = form.save(commit=False)
        self.object.imgname = image.name
        self.object.imglink = CF_GET_URL + image.name
        self.object.save()

        return JsonResponse({'message': 'Image uploaded'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)