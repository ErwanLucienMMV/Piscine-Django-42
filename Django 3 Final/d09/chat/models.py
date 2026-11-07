from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name
