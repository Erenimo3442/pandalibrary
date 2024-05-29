from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
	path('login_user', views.login_user, name='login'),
	path('logout_user', views.logout_user, name='logout'),
	path('signup_user', views.signup_user, name='signup'),
	path('profile/<str:username>', views.profile_page, name='profile'),
	path('social', views.social, name='social'),
	path('aboutus', views.aboutus, name='aboutus'),
]