from django import forms
from .models import Game, Comment


class GameForm(forms.ModelForm):
    class Meta:
        CHOICES = (
            ('PC', 'PC'),
            ('Playstation', 'Playstation'),
            ('Xbox', 'Xbox'),
            ('Mobile', 'Mobile'),
        )

        model = Game
        fields = ['title', 'developer', 'release_date', 'platform', 'genre', 'description', 'cover', 'hltb',
                  'metacritic']
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'developer': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-control'}),
            'platform': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'type': 'text', 'class': 'form-control'}),
            'cover': forms.FileInput(attrs={'type': 'file', 'class': 'form-control'}),
            'hltb': forms.URLInput(attrs={'type': 'url', 'class': 'form-control'}),
            'metacritic': forms.URLInput(attrs={'type': 'url', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['title'].initial = kwargs['initial'].get('title')
        self.fields['title'].required = False
        self.fields['developer'].required = False
        self.fields['release_date'].required = False
        self.fields['platform'].required = False
        self.fields['genre'].required = False
        self.fields['description'].required = False
        self.fields['cover'].required = False
        self.fields['hltb'].required = False
        self.fields['metacritic'].required = False
        self.fields['hltb'].label = "How Long to Beat Page"
        self.fields['metacritic'].label = "Metacritic Page"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

        widgets = {
        'comment': forms.Textarea(attrs={'type': 'text', 'class': 'form-control'})
        }

class SuggestionsForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        }
