from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from members.forms import UserGamesForm
from members.models import UserGames
from .models import Game
from .forms import GameForm
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction

# Create your views here.
def game_list(request):
    games = Game.objects.all()
    return render(request, template_name='games/game_list.html', context={'games': games})

@login_required
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

def edit_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game has been updated successfully')
            return redirect('games:game_list')
        else:
            messages.error(request, 'Error updating game. Please try again')
            return redirect('games:edit_game', game_id=game_id)
    else:
        form = GameForm(instance=game)
    return render(request, 'games/edit_game.html', {'form': form})

def delete_game(request):
    game_id = request.POST.get('game_id')
    UserGames.objects.filter(game_id=game_id, user=request.user).delete()
    return JsonResponse({'status': 'success'})


@login_required
@transaction.atomic
def update_game_status(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        new_status = request.POST.get('status')
        user_game = get_object_or_404(UserGames, user=request.user, game_id=game_id)
        user_game.status = new_status
        user_game.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})

@login_required
def delete_game(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        UserGames.objects.filter(user=request.user, game_id=game_id).delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    star_range = range(5)
    total = 0
    for object in UserGames.objects.filter(game=game):
        total += object.rating
    return render(request, 'games/game_detail.html', {'game': game, 'star_range': star_range})


@login_required
@require_POST
def rate_game(request, game_id, rating):
    if request.method == 'POST':
        game = get_object_or_404(Game, pk=game_id)
        user_game = get_object_or_404(UserGames, user=request.user, game=game)
        user_game.rating = rating
        user_game.save()

        total = 0
        for object in UserGames.objects.filter(game=game):
            total += object.rating
        game.average_rating = total / UserGames.objects.filter(game=game).count()
        game.save()
        return JsonResponse({'average_rating': user_game.rating})