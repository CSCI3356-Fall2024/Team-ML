from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
  path('oauth/', include('social_django.urls')),
  path('admin/', admin.site.urls),
  path("", views.home_view, name="home"),
  path("logout/", views.logout_view, name="logout"),
  path('profile/', views.profile_view, name='profile'),
  path('profile_create/', views.profile_create_view, name='profile_create'),
  path('profile/edit/', views.profile_edit, name='profile_edit'),
  path('check/', views.check, name='check'),
  path('landing/', views.landing_view, name='landing'),
  path('campaign_create/', views.create_campaign, name='campaign_create'),
  path('campaign_list/', views.campaign_list_view, name='campaign_list'),
  path('campaign/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
  path('campaign/<int:campaign_id>/complete/', views.complete_campaign, name='campaign_complete'),
  path('supervisor_alert/', views.supervisor_alert, name='supervisor_alert'),
  path('rewards_list/', views.reward_list_view, name='rewards_list'),
  path('rewards_create/', views.reward_create_view, name='rewards_create'),
  path('reward/<int:reward_id>/redeem/', views.redeem_reward, name='reward_redeem'),
  path('actions/', views.actions_view, name='actions'), 
  path('profile/upload_picture/', views.upload_profile_picture, name='profile_picture_upload'),
  path('news_create/', views.news_create, name='news_create')
]