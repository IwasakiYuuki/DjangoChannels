# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login, logout, get_user
import json
import cv2
from datetime import datetime, timezone
import os


def create_img_path():
    dir_path = os.path.abspath(os.path.curdir) + '/static/chat/img/'
    extention = '.png'
    time = str(datetime.now()).replace(' ', '_')
    return dir_path + time + extention


def resize_img(img, new_width):
    heigth, width, _ = img.shape
    rate = new_width / width
    width = width * rate
    heigth = heigth * rate
    img = cv2.resize(img, (int(width), int(heigth)))
    return img


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.session = self.scope['session']
        self.session.save()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        key = self.session.session_key
        user_name = self.session['user_name']
        time = datetime.now()
        time = format(time.hour, '02') + ':' + format(time.minute, '02')
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'session_key': key,
                    'user_name': user_name,
                    'time': time,
                }
            )
        elif bytes_data:
            filename = create_img_path()
            rel_path = '/'+str(os.path.relpath(filename))
            with open(filename, 'wb') as f:
                f.write(bytes_data)
#            img = cv2.imread(filename)
#            height, width, _ = img.shape
#            if width > 300:
#                img = resize_img(img, 300)
#                cv2.imwrite(filename, img)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_image',
                    'url': rel_path,
                    'session_key': key,
                    'user_name': user_name,
                    'time': time,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        data_type = event['type']
        key = event['session_key']
        # Send message to WebSocket
        message = event['message']
        user_name = event['user_name']
        time = event['time']
        await self.send(text_data=json.dumps({
            'type': data_type,
            'message': message,
            'session_key': key,
            'user_name': user_name,
            'time': time,
        }))

    # Receive message from room group
    async def chat_image(self, event):
        data_type = event['type']
        key = event['session_key']
        # Send message to WebSocket
        url = event['url']
        user_name = event['user_name']
        await self.send(text_data=json.dumps({
            'type': data_type,
            'url': url,
            'session_key': key,
            'user_name': user_name,
            'time': time,
        }))
