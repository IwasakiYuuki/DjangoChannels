from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'chat/index.html', {})


def create_user(request):
    request.session.create()
    request.session['user_name'] = request.POST.get(key='user_name')
    request.session['room_name'] = request.POST.get(key='room_name')
    return redirect('chat:room')


def room(request):
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