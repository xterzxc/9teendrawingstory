from django.urls import path, include
from .views import *

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', SignUpView.as_view(), name='signup'),
] 
