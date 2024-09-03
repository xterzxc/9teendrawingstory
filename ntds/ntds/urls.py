from django.contrib import admin
from django.urls import path, include
from .views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('draw/', include('draw.urls')),
    path('usr/', include('users.urls')),
]
