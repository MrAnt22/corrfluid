from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)

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
    value = models.IntegerField(blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.game} - {self.value}"
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

