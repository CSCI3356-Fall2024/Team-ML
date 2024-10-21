from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
  path('admin/', admin.site.urls),
  path("", views.home_view, name="home"),
  path("login/", views.login_view, name="login"),
  path("logout/", views.logout_view, name="logout"),
  path('actions/', views.actions_view, name='actions'), 
  path('rewards/', views.rewards_view, name='rewards'),
  path('profile/', views.profile_view, name='profile'),
  path('create/', views.profile_create_view, name='create'),
  path('post_google_login/', views.post_google_login_view, name='post_google_login'),
]