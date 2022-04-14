from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class SearchTerm(models.Model):
    class Meta:
        ordering = ["id"]

    term = models.TextField(unique=True)
    last_search = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.term


class Genre(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.TextField(unique=True)
    igdb_id = models.TextField(unique=True)

    def __str__(self):
        return f'{self.igdb_id}, {self.name}'

class Game(models.Model):
    class Meta:
        ordering = ["title", "year"]

    name = models.TextField()
    igdb_id = models.SlugField(unique=True)
    genres = models.ManyToManyField(Genre, related_name="games")

    def __str__(self):
        return f"{self.title} ({self.genres})"

    @property
    def url(self):
        # required for DRF to render the `url` field in the title and url game serializer
        return self.pk


class GameTime(models.Model):
    class Meta:
        ordering = ["creator", "start_time"]

    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    start_notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game} by {self.creator.email}"


class GameTimeInvitation(models.Model):
    class Meta:
        unique_together = [("invitee", "game_night")]

    game_night = models.ForeignKey(
        GameTime, on_delete=models.CASCADE, related_name="invites"
    )
    invitee = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    attendance_confirmed = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game_night} / {self.invitee.email}"
