from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login
from .models import User
from .forms import UserProfileForm

# Create your views here.

def home(request):
  return render(request, "home.html")

def login_view(request):
  return render(request, "login.html")

def logout_view(request):
  logout(request)
  return redirect("home")

def home_view(request):
  return render(request, 'home.html')

def actions_view(request):
  return render(request, 'actions.html')

def rewards_view(request):
  return render(request, 'rewards.html')

def profile_view(request):
    # Sample data to simulate user information
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'bio': 'Software developer with a passion for open-source projects.',
    }
    return render(request, 'profile.html', {'user': user_data})