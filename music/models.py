from django.db import models
from artists.models import Artist

class Music(models.Model):
    GENRE = (
        ('rnb', 'Rythm and Blues'),
        ('country', 'Country'),
        ('classic', 'Classic'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz')
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=20, choices=GENRE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['title', 'album_name']
