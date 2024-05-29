from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserGames, Game

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

class UserGamesForm(forms.ModelForm):
    class Meta:
        CHOICES = [
            ('Playing', 'Playing'),
            ('Will Play', 'Will Play'),
            ('Finished', 'Finished'),
        ]
        game = Game.objects.all()
        model = UserGames
        fields = ['game', 'status']
        widgets = {
            'game': forms.Select(choices=game, attrs={'class': 'form-control'}),
            'status': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
        }