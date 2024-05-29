from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, UserGamesForm
from .models import UserGames


from .models import UserGames



# Create your views here.
def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created and you have successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Error creating your account. Please try again')
            return redirect('members:signup')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Error logging in. Please try again')
            return redirect('members:login')
    return render(request, 'authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')

def profile_page(request, username):

    if username is None:
        user = request.user
    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('index')

    user_games = UserGames.objects.filter(user=user)
    playing_games = user_games.filter(status='playing')
    will_play_games = user_games.filter(status='will_play')
    finished_games = user_games.filter(status='finished')

    if request.method == 'POST':
        form = UserGamesForm(request.POST)
        if form.is_valid():
            user_game = form.save(commit=False)
            user_game.user = request.user
            user_game.save()
            return redirect('profile', username=username)
    else:
        form = UserGamesForm()
    context = {
        'user': user,
        'form': form,
        'playing_games': playing_games,
        'will_play_games': will_play_games,
        'finished_games': finished_games,
    }

    return render(request, 'authentication/profile.html', context)

def social(request):
    users = User.objects.all()
    return render(request, 'authentication/social.html', {'users': users})
