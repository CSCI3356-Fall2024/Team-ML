from django.urls import path
from . import views
from .views import profile_view


urlpatterns = [
  path("", views.home, name="home"),
  path("login/", views.login_view, name="login"),
  path("logout/", views.logout_view, name="logout"),
  path('home/', views.home_view, name='actions'), 
  path('actions/', views.actions_view, name='actions'), 
  path('rewards/', views.rewards_view, name='rewards'),
  path('profile/', profile_view, name='profile'),
]