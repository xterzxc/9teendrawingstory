from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', include("django.contrib.auth.urls")),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
] 
