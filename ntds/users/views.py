from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreateForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.http import JsonResponse
from ntds.utils import CF_ACCESS

class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        return next_url or reverse_lazy('index')
    

class LoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        return next_url or reverse_lazy('index')
    


class ChangeAvatarView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_avatar_default() == False:

            cf_access = CF_ACCESS()
            cf_delete, status_code = cf_access.delete(user.avatarimage)
            if status_code != 200:
                return JsonResponse(cf_delete, status=500)

            # user.avatarlink = peredannyj image
            # user.avatarimage = peredannyj image
            user.save()
            return JsonResponse({'message': 'Avatar changed'}, status=200)
        else:
            # user.avatarlink = peredannyj image
            # user.avatarimage = peredannyj image
            user.save()
            return JsonResponse({'message': 'Avatar changed'}, status=200)