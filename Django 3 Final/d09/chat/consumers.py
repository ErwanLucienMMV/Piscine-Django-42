from types import SimpleNamespace

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user
from django.contrib.sessions.backends.db import SessionStore

from .models import Room


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.joined = False
        self.user = self.scope["user"]
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.session_key = self.scope["session"].session_key
        if not self.user.is_authenticated or not await self.session_is_valid():
            await self.close(code=4401)
            return
        if not await database_sync_to_async(Room.objects.filter(pk=self.room_id).exists)():
            await self.close(code=4404)
            return
        self.room_group = "room." + str(self.room_id)
        self.session_group = "session." + self.session_key
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.channel_layer.group_add(self.session_group, self.channel_name)
        await self.accept()
        self.joined = True
        await self.broadcast({"type": "notice", "text": self.user.get_username() + " has joined the chat"})

    async def disconnect(self, close_code):
        if self.joined:
            await self.channel_layer.group_discard(self.room_group, self.channel_name)
            await self.channel_layer.group_discard(self.session_group, self.channel_name)
            self.joined = False

    @database_sync_to_async
    def session_is_valid(self):
        # Reload the session: a long-lived socket must not retain a logged-out identity.
        request = SimpleNamespace(session=SessionStore(session_key=self.session_key))
        user = get_user(request)
        return user.is_authenticated and user.pk == self.user.pk

    async def receive_json(self, content, **kwargs):
        if not await self.session_is_valid():
            await self.close(code=4401)
            return
        text = content.get("message") if isinstance(content, dict) else None
        if not isinstance(text, str) or not text.strip() or len(text) > 2000:
            await self.send_json({"type": "error", "text": "Enter a message of 1 to 2000 characters."})
            return
        await self.broadcast({"type": "message", "username": self.user.get_username(), "text": text})

    async def broadcast(self, data):
        await self.channel_layer.group_send(self.room_group, {"type": "room.event", "data": data})

    async def room_event(self, event):
        if await self.session_is_valid():
            await self.send_json(event["data"])
        else:
            await self.close(code=4401)

    async def session_logout(self, event):
        await self.close(code=4401)
