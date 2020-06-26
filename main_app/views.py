from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Game, User, Profile, Photo, Review
from .forms import ReviewForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'gamefaves'

@login_required
def add_photo(request, game_id):
  photo_file = request.FILES.get('photo-file', None)
  game_photo = Photo.objects.filter(game=game_id)
  if not game_photo:
    if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        photo = Photo(url=url, game_id=game_id)
        photo.save()
      except:
        print('An error occurred uploading file to S3')
  return redirect('detail', game_id=game_id)

@login_required
def delete_photo(request, game_id):
  game_photo = Photo.objects.get(game=game_id)
  game_photo.delete()
  return redirect('detail', game_id=game_id)

def home(request):
  games = Game.objects.all()
  context = {
    'games': games
  }
  return render(request, 'home.html', context)

def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  reviews = Review.objects.filter(game=game_id)
  review_form = ReviewForm()
  photo = Photo.objects.filter(game_id=game_id)
  if request.user.username:
    user_fav_games = Profile.objects.get(user_id=request.user.id).fav_games.all()
  else:
    user_fav_games = {}
  context = {
    'photo': photo,
    'game': game,
    'user_fav_games': user_fav_games,
    'reviews': reviews,
    'review_form': review_form
  }
  return render(request, 'games/detail.html', context)

# Review work
@login_required
def add_review(request, game_id):
  review = ReviewForm(request.POST)
  if review.is_valid():
      new_review = review.save(commit=False)
      new_review.game_id = game_id
      new_review.save()
  return redirect('detail', game_id)

@login_required
def delete_review(request, game_id, review_id):
  review = Review.objects.get(id=review_id)
  review.delete()
  return redirect('detail', game_id)

@login_required
def assoc_favgame(request, game_id, user_id):
  game = Game.objects.get(id=game_id)
  Profile.objects.get(user_id=user_id).fav_games.add(game)
  return redirect('user_detail', user_id)

@login_required
def unassoc_favgame(request, game_id, user_id):
  game = Game.objects.get(id=game_id)
  profile = Profile.objects.get(user_id=user_id)
  profile.fav_games.remove(game)
  return redirect('user_detail', user_id)

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