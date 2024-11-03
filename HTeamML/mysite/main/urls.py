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
  path('profile_create/', views.profile_create_view, name='profile_create'),
  path('check/', views.check, name='check'),
  path('landing/', views.landing_view, name='landing'),
  path('campaign_create/', views.create_campaign, name='campaign_create'),
  path('campaign_list/', views.campaign_list_view, name='campaign_list'),
  path('campaign/<int:campaign_id>/complete/', views.complete_campaign, name='campaign_complete')

]