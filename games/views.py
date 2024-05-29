from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from members.forms import UserGamesForm
from members.models import UserGames
from .models import Game, Comment, GameSuggestion
from .forms import GameForm, CommentForm, SuggestionsForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction


# Create your views here.
def game_list(request):
    games = Game.objects.all()
    return render(request, template_name='games/game_list.html', context={'games': games})


@login_required
def add_game(request, game_id=None):
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
            return redirect('members:profile', username=request.user.username)
        else:
            messages.error(request, 'Error adding game to your profile. Please try again')
            return redirect('games:add_game')
    else:
        if game_id:
            game = get_object_or_404(Game, pk=game_id)
            form = UserGamesForm(initial={'game': game})
        else:
            form = UserGamesForm()

    return render(request, 'games/add_games.html', {'form': form, 'games': games})


def game_create(request, suggestion_id=None):
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
        if suggestion_id:
            suggestion = get_object_or_404(GameSuggestion, pk=suggestion_id)
            form = GameForm(initial={'title': suggestion.title})
            suggestion.delete()
        else:
            form = GameForm()
    return render(request, 'games/game_create.html', {'form': form})


def edit_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if 'action' in request.POST and request.POST['action'] == 'delete':
            game.delete()
            messages.success(request, 'Game has been deleted successfully')
            return redirect('games:game_list')
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
def remove_game(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        UserGames.objects.filter(user=request.user, game_id=game_id).delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    comments = game.comments.all()
    new_comment = None
    star_range = range(5)
    if request.user.is_authenticated:
        user_has_game = UserGames.objects.filter(user=request.user, game=game).exists()
    else:
        user_has_game = False

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.game = game
            new_comment.save()
            return HttpResponseRedirect(reverse('games:game_detail', kwargs={'game_id': game.pk}))
    else:
        comment_form = CommentForm()

    return render(request, 'games/game_detail.html',
                  {'game': game,
                   'star_range': star_range,
                   'user_has_game': user_has_game,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


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
            try:
                total += object.rating
            except:
                pass
        game.average_rating = total / UserGames.objects.filter(game=game).count()
        game.save()
        return JsonResponse({'average_rating': user_game.rating})


def game_suggestions(request):
    suggestions = GameSuggestion.objects.all()
    return render(request, 'games/game_suggestions.html', {'suggestions': suggestions})


def suggestion_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        suggestion = GameSuggestion(title=title, suggested_by=request.user)
        suggestion.save()
        messages.success(request, 'Suggestion has been created successfully')
        return redirect('games:game_list')
    else:
        form = SuggestionsForm()
    return render(request, 'games/suggestion_create.html', {'form': form})
