from django.contrib import admin
from .models import Game, Assessment, FriendRequest, User

admin.site.register(Game)
admin.site.register(Assessment)
admin.site.register(FriendRequest)
admin.site.register(User)