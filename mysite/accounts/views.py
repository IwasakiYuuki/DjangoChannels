from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from oauthlib.oauth2 import MissingCodeError
from django.conf import settings
import google_auth_oauthlib


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


def profile(request):
    return render(request, 'chat/index.html', {})
