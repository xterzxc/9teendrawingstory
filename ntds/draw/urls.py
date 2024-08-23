from django.urls import path, include
from .views import *


urlpatterns = [
    path('', DrawingView, name='draw'),
    path('create/', DrawingCreateView.as_view(), name='draw-create'),
]
