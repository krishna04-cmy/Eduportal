# ye WebSocket ka main code hai:

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, Message, UserStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Space ko underscore se replace karo
        self.room_group_name = f'chat_{self.room_name.replace(" ", "_")}'

        # Room group join karo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # User online mark karo
        if self.scope['user'].is_authenticated:
            await self.set_user_online(self.scope['user'], True)

        await self.accept()

    async def disconnect(self, close_code):
        # User offline mark karo
        if self.scope['user'].is_authenticated:
            await self.set_user_online(self.scope['user'], False)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username

        # Message save karo
        await self.save_message(self.scope['user'], self.room_name, message)

        # Group ko message bhejo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, content):
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        Message.objects.create(room=room, sender=user, content=content)

    @database_sync_to_async
    def set_user_online(self, user, status):
        UserStatus.objects.update_or_create(
            user=user,
            defaults={'is_online': status}
        )