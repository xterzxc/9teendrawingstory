import debug_toolbar
from .settings import DEBUG_TOOLBAR
from django.contrib import admin
from django.urls import path, include
from .views import IndexView, LoadDrawingsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('draw/', include('draw.urls')),
    path('usr/', include('users.urls')),
    path('load-drawings/', LoadDrawingsView.as_view(), name='load-drawings'),
]

if DEBUG_TOOLBAR:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]