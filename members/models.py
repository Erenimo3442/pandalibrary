from django.db import models
from django.contrib.auth.models import User
from games.models import Game

# Create your models here.

class UserGames(models.Model):
    STATUS_CHOICES = [
        ('playing', 'Playing'),
        ('will_play', 'Will Play'),
        ('finished', 'Finished'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'game')
