# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login, logout, get_user
import random
import json
import cv2


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
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            key = text_data_json['session_key']
            print(self.session.session_key)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'session_key': key
                }
            )
        elif bytes_data:
            filename = 'static/chat/test2.png'
            width, heigth = (300, 160)
            with open(filename, 'wb') as f:
                f.write(bytes_data)
            img = cv2.imread(filename)
            img = cv2.resize(img, (width, heigth))
            cv2.imwrite(filename, img)




    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        key = event['session_key']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'session_key': key
        }))

