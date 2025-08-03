from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name="register"),
    path('gallery/', views.gallery, name="gallery"),
    path('searched_games/', views.search, name="searched_games"),
    path('game/<int:pk>', views.game, name="game"),
    path('user_total/<int:pk>', views.user_total, name="user-total"),
    path('list/', views.list, name='list'),
    path('game_detail/<int:pk>', views.game_detail, name="game_detail"),
    path('gd_iframe/<int:pk>', views.game_detail_iframe, name="gd-iframe"),
    path('about/', views.about, name='about')
]
