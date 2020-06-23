from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, User, Profile

def home(request):
  games = Game.objects.all()
  context = {
    'games': games
  }
  return render(request, 'home.html', context)

def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  if request.user.username:
    user_fav_games = Profile.objects.get(user_id=request.user.id).fav_games.all()
  else:
    user_fav_games = {}
  context = {
    'game': game,
    'user_fav_games': user_fav_games,
  }
  return render(request, 'games/detail.html', context)

@login_required
def assoc_favgame(request, game_id, user_id):
  game = Game.objects.get(id=game_id)
  Profile.objects.get(user_id=user_id).fav_games.add(game)
  user = User.objects.get(id=user_id)
  fav_games = Profile.objects.get(user_id=user_id).fav_games.all()
  context = {
    'user': user,
    'fav_games': fav_games,
  }
  return render(request, 'user.html', context)

@login_required
def unassoc_favgame(request, game_id, user_id):
  game = Game.objects.get(id=game_id)
  profile = Profile.objects.get(user_id=user_id)
  profile.fav_games.remove(game)
  user = User.objects.get(id=user_id)
  fav_games = profile.fav_games.all()
  context = {
    'user': user,
    'game': game,
    'fav_games': fav_games,
  }
  return render(request, 'user.html', context)


class GameCreate(LoginRequiredMixin, CreateView):
  model = Game
  fields = ['name', 'genre']
  def form_valid(self,form):
    form.instance.added_by = self.request.user
    return super().form_valid(form)

@login_required
def game_delete(request, game_id):
  game = Game.objects.get(id=game_id)
  if request.user == game.added_by:
    game.delete()
  return redirect('home')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      Profile(user_id = user.id).save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def user_detail(request, user_id):
  user = User.objects.get(id=user_id)
  fav_games = Profile.objects.get(user_id=user_id).fav_games.all()
  context = {
    'user': user,
    'fav_games': fav_games,
  }
  return render(request, 'user.html', context)