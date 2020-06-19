from django.db import models
from django.urls import reverse

GENRES = (
    ('A', 'Action'),
    ('R', 'Role-Playing'),
    ('P', 'Puzzle'),
    ('S', 'Sports'),
)

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=20)
    genre = models.CharField(
        max_length=1,
        choices=GENRES,
        default=GENRES[0][0],
    )
    added_by = models.CharField(max_length=20)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})
