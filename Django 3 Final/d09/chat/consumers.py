import asyncio
import json
from dataclasses import dataclass, field
from types import SimpleNamespace

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user
from django.contrib.sessions.backends.db import SessionStore

from .models import Message, Room


@dataclass
class RoomState:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    members: dict = field(default_factory=dict)


# One ASGI process owns presence and serializes each room's events.
room_states = {}


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
        self.state = room_states.setdefault(self.room_id, RoomState())
        async with self.state.lock:
            history = await self.recent_messages()
            await self.channel_layer.group_add(self.room_group, self.channel_name)
            await self.channel_layer.group_add(self.session_group, self.channel_name)
            await self.accept()
            await self.send_json({"type": "history", "messages": history})
            self.state.members[self.channel_name] = self.user.get_username()
            self.joined = True
            await self.broadcast({
                "type": "notice", "text": self.user.get_username() + " has joined the chat",
                "users": self.current_users(),
            })

    async def disconnect(self, close_code):
        if self.joined:
            async with self.state.lock:
                await self.channel_layer.group_discard(self.room_group, self.channel_name)
                await self.channel_layer.group_discard(self.session_group, self.channel_name)
                self.state.members.pop(self.channel_name, None)
                self.joined = False
                username = self.user.get_username()
                if username not in self.state.members.values():
                    await self.broadcast({
                        "type": "notice", "text": username + " has left the chat",
                        "users": self.current_users(),
                    })

    def current_users(self):
        return sorted(set(self.state.members.values()), key=str.casefold)

    @database_sync_to_async
    def recent_messages(self):
        messages = list(Message.objects.filter(room_id=self.room_id).order_by("-pk")[:3])
        return [{"username": message.username, "text": message.text} for message in reversed(messages)]

    @database_sync_to_async
    def store_message(self, text):
        Message.objects.create(room_id=self.room_id, author=self.user, username=self.user.get_username(), text=text)

    @database_sync_to_async
    def session_is_valid(self):
        # Reload the session: a long-lived socket must not retain a logged-out identity.
        request = SimpleNamespace(session=SessionStore(session_key=self.session_key))
        user = get_user(request)
        return user.is_authenticated and user.pk == self.user.pk

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if bytes_data is not None:
            await self.send_json({"type": "error", "text": "Send a JSON text message."})
            return
        try:
            await super().receive(text_data=text_data, bytes_data=bytes_data, **kwargs)
        except json.JSONDecodeError:
            await self.send_json({"type": "error", "text": "Send a valid JSON message."})

    async def receive_json(self, content, **kwargs):
        if not await self.session_is_valid():
            await self.close(code=4401)
            return
        text = content.get("message") if isinstance(content, dict) else None
        if not isinstance(text, str) or not text.strip() or len(text) > 2000:
            await self.send_json({"type": "error", "text": "Enter a message of 1 to 2000 characters."})
            return
        async with self.state.lock:
            await self.store_message(text)
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
