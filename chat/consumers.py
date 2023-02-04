import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from channels.auth import login
from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]['kwargs']["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_user(self):
        return self.scope['user']

    async def disconnect(self, code_code):
        await self.channel_layer.group_dsicard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        user = await self.get_user()
        await database_sync_to_async(self.scope["session"].save)()
        await login(self.scope, user)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(user=user, message=message)
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )
        # self.send(text_data=json.dumps({'message': message}))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def save_message(self, user, message):
        ChatMessage.objects.create(user_id=user, message=message)
