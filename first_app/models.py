from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    description = models.TextField(blank=True, null=True)
    screenshots = models.URLField(blank=True)
    genres = models.CharField(max_length=255, blank=True)
    developers = models.CharField(max_length=255, blank=True)
    publishers = models.CharField(max_length=255, blank=True)
    trailer_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return  self.name
    
class Assessment(models.Model):
    value = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.game} - {self.value}"