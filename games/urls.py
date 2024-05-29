from django.urls import path
from members.views import profile_page
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'games'

urlpatterns = [
	path('add_game/', views.add_game, name='add_game'),
	path('add_game/<int:game_id>', views.add_game, name='add_game_with_id'),
	path('game_list/', views.game_list, name='game_list'),
	path('game_create/', views.game_create, name='game_create'),
	path('game_create/<int:suggestion_id>', views.game_create, name='game_create_with_suggestion'),
	path('game_suggestions/', views.game_suggestions, name='game_suggestions'),
	path('suggestion_create/', views.suggestion_create, name='suggestion_create'),
	path('remove_game/', views.remove_game, name='remove_game'),
	path('update_game_status/', views.update_game_status, name='update_game_status'),
	path('game/<int:game_id>/', views.game_detail, name='game_detail'),
	path('game/<int:game_id>/edit', views.edit_game, name='edit_game'),
	path('game/<int:game_id>/rate_game/<int:rating>', views.rate_game, name='rate_game'),
]