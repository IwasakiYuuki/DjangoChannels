from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
import google_auth_oauthlib.flow
from django.conf import settings
from oauthlib.oauth2 import MissingCodeError
from .models import Profile
from django.contrib.auth.decorators import login_required


def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    name = None
    if hasattr(user, 'profile'):
        pass
    else:
        if backend.name == 'google-oauth2':
            print(response)
            url = response['picture']
            name = response['name']
        if url and name:
            profile = Profile.objects.create(
                avatar=url,
                user_name=name,
                user=user
            )
            profile.save()
