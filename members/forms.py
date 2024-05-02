from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserGames, Game

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserGamesForm(forms.ModelForm):
    game = forms.ModelChoiceField(queryset=Game.objects.all())

    class Meta:
        model = UserGames
        fields = ['game', 'status']