from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("login/", views.login_view, name="login"),
  path("logout/", views.logout_view, name="logout"),
  path('actions/', views.actions_view, name='actions'), 
  path('rewards/', views.rewards_view, name='rewards'),
  path('profile/', views.rewards_view, name='profile'),
]