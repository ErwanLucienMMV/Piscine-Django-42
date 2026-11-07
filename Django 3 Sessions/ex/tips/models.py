from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    @property
    def reputation(self):
        if not self.pk:
            return 0
        return Vote.objects.filter(tip__author_id=self.pk).aggregate(
            score=models.Sum(models.Case(
                models.When(value=Vote.UP, then=5),
                models.When(value=Vote.DOWN, then=-2),
                default=0,
                output_field=models.IntegerField(),
            ))
        )["score"] or 0

    def can_delete_tip(self, tip):
        return self.is_active and (tip.author_id == self.pk or self.has_perm("tips.delete_tip"))

    def can_downvote_tip(self, tip):
        return self.is_active and (tip.author_id == self.pk or self.has_perm("tips.downvote_tip"))


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tips")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-pk"]
        permissions = [("downvote_tip", "Can downvote tips")]

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
