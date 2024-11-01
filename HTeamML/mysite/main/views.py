from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from .forms import UserProfileForm, CampaignForm
from .models import User, Campaign



# Create your views here.


def logout_view(request):
  logout(request)
  return redirect("home")

def home_view(request):
  return render(request, 'home.html')

def actions_view(request):
  return render(request, 'actions.html')

def rewards_view(request):
  return render(request, 'rewards.html')

def landing_view(request):
   return render(request, 'landing.html')

 

def profile_view(request):
  user = get_object_or_404(User, email=request.user.email)
  context = {
        'user': user
  }
  return render(request, 'profile.html', context)

def profile_create_view(request):
  email = request.user.email

  if request.method == 'POST':
    form = UserProfileForm(request.POST)
        
    if form.is_valid():
      profile = form.save(commit=False)
      profile.email = email
      profile.profile_completed = True
      profile.save()  
      return redirect('profile') 
  else:
    form = UserProfileForm(initial={'email': email})

    context = {
      'form': form
    }
    return render(request, "profile_create.html", context)
  

def check(request):
    google_email = request.user.email
  
    if User.objects.filter(email=google_email).exists():
        existing_user = User.objects.get(email=google_email)
        return redirect('profile')  
    else:
        return redirect('profile_create')  
    



@login_required
def campaign_list_view(request):
  current_date = timezone.now().date()
    
  user_email = request.user.email
  user = User.objects.filter(email=user_email).first()
    
  expired_campaigns = Campaign.objects.filter(enddate__lt=current_date)
  active_campaigns = Campaign.objects.filter(enddate__gte=current_date)

  return render(request, 'campaign_list.html', {
    'user': user,
    'expired_campaigns': expired_campaigns,
    'active_campaigns': active_campaigns
  })


def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = CampaignForm()

    return render(request, 'campaign_create.html', {'form': form})