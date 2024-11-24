from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

from .forms import UserProfileForm, CampaignForm, RewardForm
from .models import User, Campaign, CampaignCompletionInfo, Reward


@login_required 
def get_user(request):
  return User.objects.filter(email=request.user.email).first()

@login_required 
def supervisor_check(request):
  user = get_user(request)
  if user is None or not user.supervisor:
    return redirect('supervisor_alert')  

  return None

def supervisor_alert(request):
  return render(request, 'supervisor_alert.html')

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
        return redirect('profile')  
    else:
        return redirect('profile_create')  

@login_required
def campaign_list_view(request):
  current_date = timezone.now().date()

  user = get_user(request)

  expired_campaigns = Campaign.objects.filter(enddate__lt=current_date)
  active_campaigns = Campaign.objects.filter(enddate__gte=current_date)

  return render(request, 'campaign_list.html', {
    'user': user,
    'expired_campaigns': expired_campaigns,
    'active_campaigns': active_campaigns
  })

def create_campaign(request):
    if supervisor_check(request):
      return supervisor_check(request)
    
    user = get_user(request)

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list') 
    else:
        form = CampaignForm()

    return render(request, 'campaign_create.html', {
        'form': form,
        'user': user 
    })

@login_required
def complete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    user = get_user(request)

    if campaign not in user.completed_campaigns.all():
        user.completed_campaigns.add(campaign)
        user.update_points()
        user.save()
        
        CampaignCompletionInfo.objects.create(user=user, campaign=campaign)
        
        return redirect('campaign_list')
    else:
        messages.info(request, f"Error: Campaign '{campaign.name}' is already completed.")

@login_required
def campaign_detail(request, campaign_id):
  campaign = get_object_or_404(Campaign, id=campaign_id)
    
  campaign_completion_list = CampaignCompletionInfo.objects.filter(campaign_id = campaign.id)
    
  return render(request, 'campaign_detail.html', {
    'campaign': campaign,
    'campaign_completion_list': campaign_completion_list,
  })


def landing_view(request):
    top_users = User.objects.order_by('-total_points')[:5]
    
    return render(request, 'landing.html', {'top_users': top_users})

@login_required
def reward_list_view(request):
    current_date = timezone.now().date()
    
    user = get_user(request)
   
    active_rewards = Reward.objects.filter(enddate__gte=current_date)
    expired_rewards = Reward.objects.filter(enddate__lt=current_date)

    return render(request, 'rewards.html', {
      'user': user, 
      'active_rewards': active_rewards,
      'expired_rewards': expired_rewards,
    })


@login_required
def reward_create_view(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reward_list')
    else:
        form = RewardForm()

    return render(request, 'rewards_create.html', {
        'form': form,
        'user': request.user
    })