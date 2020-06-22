from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game

def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', { 'games': games })

def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  return render(request, 'games/detail.html', { 'game': game })

class GameCreate(LoginRequiredMixin, CreateView):
  model = Game
  fields = ['name', 'genre']
  def form_valid(self,form):
    form.instance.added_by = self.request.user
    return super().form_valid(form)

class GameDelete(LoginRequiredMixin, DeleteView):
  model = Game
  success_url = '/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)