from django.shortcuts import render
from django.views import View

def DrawView(request):
    
    return render(request, 'draw/draw.html')