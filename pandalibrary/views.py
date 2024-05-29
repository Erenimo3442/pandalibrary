from django.shortcuts import render
from games.models import Game
from members.models import UserGames


# Create your views here.
def index(request):
    highest_rates = Game.objects.order_by('-average_rating')[:4]
    latest_releases = Game.objects.order_by('-release_date')[:4]
    return render(request, template_name='index.html', context={'highest_rates': highest_rates, 'latest_releases': latest_releases})
