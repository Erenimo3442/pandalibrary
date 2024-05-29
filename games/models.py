from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
    STATUS_CHOICES = [
        ('PC', 'PC'),
        ('Playstation', 'Playstation'),
        ('Xbox', 'Xbox'),
        ('Mobile', 'Mobile'),
    ]
    title = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', blank=True, null=True)
    average_rating = models.FloatField(default=0)
    hltb = models.CharField(max_length=100, blank=True)
    metacritic = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title + ' by ' + self.developer


class Comment(models.Model):
    game = models.ForeignKey(Game, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Comment by {self.user.username} on {self.game.title}"


class GameSuggestion(models.Model):
    title = models.CharField(max_length=100)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' suggested by ' + self.suggested_by.username