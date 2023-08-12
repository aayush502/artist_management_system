from django.db import models

class Artist(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )

    name = models.CharField(max_length=255)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDER)
    address = models.CharField(max_length=255)
    first_release_year = models.DateTimeField()
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['name', 'dob', 'first_relaese_year', 'no_of_albums_released']

    def __str__(self):
        return self.name
