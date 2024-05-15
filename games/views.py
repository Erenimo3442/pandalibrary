import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from members.forms import UserGamesForm
from members.models import UserGames
from .models import Game
from .forms import GameForm
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
def game_list(request):
    games = Game.objects.all()
    return render(request, template_name='games/game_list.html', context={'games': games})


def add_game(request):
    games = Game.objects.all()
    if request.method == 'POST':
        form = UserGamesForm(request.POST)
        if form.is_valid():
            user_game = form.save(commit=False)
            user_game.user = request.user
            if UserGames.objects.filter(user=user_game.user, game=user_game.game).exists():
                messages.error(request, 'This game is already added to your profile')
                return redirect('games:add_game')
            user_game.save()
            messages.success(request, 'Game has been added to your profile')
            return redirect('members:profile')
        else:
            messages.error(request, 'Error adding game to your profile. Please try again')
            return redirect('games:add_game')
    else:
        form = UserGamesForm()

    return render(request, 'games/add_games.html', {'form': form, 'games': games})


def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            developer = request.POST.get('developer')
            release_date = request.POST.get('release_date')
            platform = request.POST.get('platform')
            genre = request.POST.get('genre')
            description = request.POST.get('description')
            cover = request.FILES.get('cover')
            game = Game(title=title, description=description,
                        developer=developer, release_date=release_date,
                        platform=platform, genre=genre, cover=cover)
            game.save()
            messages.success(request, 'Game has been created successfully')
            return redirect('games:game_list')
        else:
            print(form.errors)
            messages.error(request, 'Error creating game. Please try again')
            return redirect('games:game_create')
    else:
        form = GameForm()
    return render(request, 'games/game_create.html', {'form': form})

def delete_game(request):
    game_id = request.POST.get('game_id')
    UserGames.objects.filter(game_id=game_id, user=request.user).delete()
    return JsonResponse({'status': 'success'})


logger = logging.getLogger((__name__))


@login_required
def update_game_status(request):
    if request.method == 'POST':
        try:
            game_id = request.POST.get('game_id')
            new_status = request.POST.get('status')
            user_game = get_object_or_404(UserGames, user=request.user, game_id=game_id)
            user_game.status = new_status
            user_game.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'status': 'failed'})
    else:
        return JsonResponse({'status': 'failed'})

@login_required
def delete_game(request):
    if request.method == 'POST':
        try:
            game_id = request.POST.get('game_id')
            UserGames.objects.filter(user=request.user, game_id=game_id).delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'status': 'failed'})
    else:
        return JsonResponse({'status': 'failed'})

def game_detail(request, game_i):
    game = get_object_or_404(Game, pk=game_i)
    return render(request, 'games/game_detail.html', {'game': game})
