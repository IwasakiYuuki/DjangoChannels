from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
import google_auth_oauthlib.flow
from django.conf import settings
from oauthlib.oauth2 import MissingCodeError
from .models import Credentials
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return render(request, 'chat/index.html', {})


def create_user(request):
    print(request.user)
    print(request.user.profile)
    print(request.user.profile.avatar)
    request.session.create()
    request.session['user_name'] = request.POST.get(key='user_name')
    request.session['room_name'] = request.POST.get(key='room_name')
    return redirect('chat:room')


def room(request):
    print(request.user.id)
    print(request.user.profile)
    print(request.user.profile.avatar)
    key = request.session.session_key or None
    if key:
        room_name = request.session['room_name']
        key = mark_safe(json.dumps(key))
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'session_key': key,
        })
    else:
        return render(request, 'chat/index.html', {})


def test(request):
    return render(request, 'chat/test.html', {})


@login_required
def auth(request):
    print('aaa')
    print(request.user)
    print(type(request.user))
    if hasattr(request.user, 'credentials'):
        print('aaa')
        return render(request, 'chat/index.html', {})

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRET, settings.SCOPES
    )
    flow.redirect_uri = settings.REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        approval_prompt='force',
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    print(authorization_url)
    return redirect(authorization_url)


@login_required
def callback(request):
    if hasattr(request.user, 'credentials'):
        return render(request, 'chat/index.html', {})

    print(type(request.user))
    print(request.user)
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRET, settings.SCOPES, state=state
    )
    flow.redirect_uri = settings.REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    try:
        flow.fetch_token(authorization_response=authorization_response)
    except MissingCodeError:
        pass
    else:
        print(request.user + ' unko')
        Credentials.objects.create(
            token=flow.credentials.token,
            refresh_token=flow.credentials.refresh_token or '',
            token_uri=flow.credentials.token_uri,
            client_id=flow.credentials.client_id,
            client_secret=flow.credentials.client_secret,
            scopes=flow.credentials.scopes,
            user=request.user
        )
    return render(request, 'chat/room.html', {})

