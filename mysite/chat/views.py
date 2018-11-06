from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    request.session.create()
    key = mark_safe(json.dumps(request.session.session_key))
    print(request.session.session_key)
    print(type(mark_safe(json.dumps(room_name))))
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'session_key': key,
    })
