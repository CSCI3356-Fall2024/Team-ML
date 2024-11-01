from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
  path('admin/', admin.site.urls),
  path("", views.home_view, name="home"),
  path("logout/", views.logout_view, name="logout"),
  path('actions/', views.actions_view, name='actions'), 
  path('rewards/', views.rewards_view, name='rewards'),
  path('profile/', views.profile_view, name='profile'),
  path('create/', views.profile_create_view, name='create'),
  path('check/', views.check, name='check'),
  path('landing/', views.landing_view, name='landing'),
  path('campaign/', views.create_campaign, name='campaign')
]