from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

GENRES = (
    ('A', 'Action'),
    ('R', 'Role-Playing'),
    ('P', 'Puzzle'),
    ('S', 'Sports'),
)

class Game(models.Model):
    name = models.CharField(max_length=20)
    genre = models.CharField(
        max_length=1,
        choices=GENRES,
        default=GENRES[0][0],
    )
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fav_games = models.ManyToManyField(Game)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for game_id: {self.game_id} @{self.url}"

