from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    release_date = forms.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Game
        fields = ['title', 'developer', 'release_date', 'platform', 'genre', 'description', 'cover']

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['developer'].required = False
        self.fields['release_date'].required = False
        self.fields['platform'].required = False
        self.fields['genre'].required = False
        self.fields['description'].required = False
        self.fields['cover'].required = False