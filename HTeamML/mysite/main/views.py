from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def home(request):
  return render(request, "home.html")

def login_view(request):
  return render(request, "login.html")

def logout_view(request):
  logout(request)
  return redirect("home")

def actions_view(request):
  return render(request, 'actions.html')

def rewards_view(request):
  return render(request, 'rewards.html')

def profile_view(request):
  return render(request, 'profile.html')