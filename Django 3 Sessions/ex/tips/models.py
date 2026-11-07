from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tips")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-pk"]

    def __str__(self):
        return self.content[:80]


class Vote(models.Model):
    UP = 1
    DOWN = -1
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=[(UP, "Upvote"), (DOWN, "Downvote")])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tip", "user"], name="one_vote_per_user_and_tip"),
            models.CheckConstraint(condition=models.Q(value__in=[-1, 1]), name="valid_vote_value"),
        ]
