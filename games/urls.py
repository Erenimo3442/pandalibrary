from django.urls import path
from members.views import profile_page
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'games'

urlpatterns = [
	path('add_game/', views.add_game, name='add_game'),
	path('game_list', views.game_list, name='game_list'),
	path('game_create/', views.game_create, name='game_create'),
	path('delete_game/', views.delete_game, name='delete_game'),
	path('update_game_status/', views.update_game_status, name='update_game_status'),
]