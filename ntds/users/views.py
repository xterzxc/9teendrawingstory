from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreateForm

class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"