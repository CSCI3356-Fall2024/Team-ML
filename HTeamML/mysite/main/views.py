from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage

from .forms import UserProfileForm, CampaignForm, RewardForm, NewsItemForm
from .models import User, Campaign, CampaignCompletionInfo, Reward, RewardRedeemInfo, NewsItem


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

@login_required
def upload_profile_picture(request):
    user = get_object_or_404(User, email=request.user.email)
    
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        user.profile_picture = profile_picture
        user.save()
        messages.success(request, "Profile picture updated successfully!")
        return redirect('profile')
    else:
        messages.error(request, "Please select a valid image file.")
        return redirect('profile')
    
@login_required 
def profile_view(request):
  user = get_object_or_404(User, email=request.user.email)
  context = {
        'user': user
  }
  return render(request, 'profile.html', context)

@login_required 
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

@login_required
def profile_edit(request):
    user = get_object_or_404(User, email=request.user.email)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'profile_edit.html', context)


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

@login_required 
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
        messages.success(request, f"Successfully Completed {campaign.name} ")
        return redirect('campaign_list')
    else:
        messages.error(request, f"Error: Campaign '{campaign.name}' is already completed.")

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
    user = get_user(request)
    try:
        latest_news = NewsItem.objects.latest('created_at')  
    except NewsItem.DoesNotExist:
        latest_news = None
    return render(request, 'landing.html', {
        'top_users': top_users,
        'latest_news': latest_news,
        'user': user
    })

@login_required
def reward_list_view(request):
    user = get_user(request) 
    
    active_rewards = Reward.objects.filter(expired=False)
    expired_rewards = Reward.objects.filter(expired=True)

    reward_redemption_counts = {}

    reward_data = []
    for reward in active_rewards:
        reward.update_reward()
        redemption_count = RewardRedeemInfo.objects.filter(user=user, reward=reward).count()
        reward_redemption_counts[reward.id] = redemption_count
        
        remaining_amount = reward.totalamount - reward.redeemedamount
        user_remaining_amount = reward.userredeemlimit - redemption_count
        
        reward_data.append({
            'reward': reward,
            'remaining_amount': remaining_amount,
            'redemption_count': redemption_count,
            'user_remaining_amount': user_remaining_amount
        })

    return render(request, 'rewards.html', {
        'user': user, 
        'active_rewards': reward_data,
        'expired_rewards': expired_rewards,
        'reward_redemption_counts': reward_redemption_counts,
    })


@login_required
def reward_create_view(request):
  if supervisor_check(request):
      return supervisor_check(request)
    
  user = get_user(request)
  if request.method == 'POST':
      form = RewardForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
          return redirect('rewards_list')
  else:
      form = RewardForm()

  return render(request, 'rewards_create.html', {
      'form': form,
      'user': request.user
})
    
@login_required
def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)

    user = get_user(request)
    user.update_points()
    
    if user.current_points < reward.pointsrequired:
        messages.warning(request, "Not enough Points!")
        return redirect('rewards_list') 

    user_redeemed_amount = RewardRedeemInfo.objects.filter(user=user, reward=reward).count()
    total_redeemed_amount = RewardRedeemInfo.objects.filter(reward=reward).count()
    
    if user_redeemed_amount < reward.userredeemlimit and total_redeemed_amount < reward.totalamount:
        RewardRedeemInfo.objects.create(user=user, reward=reward)
        reward.update_reward()
        user.update_points()
        user.save()
        messages.success(request, f"Successfully Redeemed {reward.name}!")
        return redirect('rewards_list')
    else:
        messages.error(request, f"Error: Reward '{reward.name}' is already redeemed.")
        return redirect('rewards_list')
        
        
@login_required
def actions_view(request):
    user = get_object_or_404(User, email=request.user.email)
    
    activities = user.activity_list()
    
    return render(request, 'actions.html', {
        'user': user,
        'activities': activities,
    })

@login_required
def news_create(request):
    user = get_user(request)

    if request.method == 'POST':
        form = NewsItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = NewsItemForm()

    return render(request, 'news_create.html', {'form': form, 'user': user})
