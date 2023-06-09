from django.shortcuts import render
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Message
from users.models import User


def room(request, room_name):
    # Fetch messages related to the chat room
    messages = Message.objects.filter(room_name=room_name)
    return render(request, "chat/room.html", {"room_name": room_name, "messages": messages})


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        message = text_data_json["message"]

        member = await sync_to_async(User.objects.get)(username=username)
        await sync_to_async(Message.objects.create)(
            room_name=self.room_name, author=member, content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "username": username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))

