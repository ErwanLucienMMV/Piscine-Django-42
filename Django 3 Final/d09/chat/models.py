from django.conf import settings
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=150)
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["pk"]
