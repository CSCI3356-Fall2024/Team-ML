from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings

class User(models.Model):
    gradYearOptions = [(2025, "2025"), (2026, "2026"), (2027, "2027"), (2028, "2028"),]

    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    school = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False)
    major = models.CharField(max_length=255, blank=False, null=False)
    minor = models.CharField(max_length=255, blank=True)
    gradyear = models.PositiveIntegerField(choices = gradYearOptions, blank=False, null=False)
    current_points = models.PositiveIntegerField(default=0, null=False)
    total_points = models.PositiveIntegerField(default=0, null=False)
    profile_completed = models.BooleanField(default=False)
    supervisor = models.BooleanField(default=False)
    completed_campaigns = models.ManyToManyField('Campaign', related_name='users', blank=True)
    redeemed_rewards = models.ManyToManyField('Reward', related_name='users', blank=True)

    
    
    def update_points(self):
        total_campaign_points = self.completed_campaigns.aggregate(total=Sum('pointsreward'))['total'] or 0
        total_redeemed_points = self.redeemed_rewards.aggregate(total=Sum('pointsrequired'))['total'] or 0
        self.total_points = total_campaign_points
        self.current_points = total_campaign_points - total_redeemed_points
        
        
    def activity_list(self):
        campaign_activities = [
           (completion.campaign.name, completion.campaign.pointsreward, completion.completed_at)
            for completion in CampaignCompletionInfo.objects.filter(user=self)
        ]
    
        reward_activities = [
            (redeem.reward.name, -redeem.reward.pointsrequired, redeem.redeemed_at)
            for redeem in RewardRedeemInfo.objects.filter(user=self)
        ]
    
        activities = campaign_activities + reward_activities
        return sorted(activities, key=lambda x: x[2])
            
        
        
            
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email
    
    
    
class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length= 255, blank=False, null=False)
    startdate = models.DateField(blank=False, null=False)
    enddate = models.DateField(blank=False, null=False)
    pointsreward = models.PositiveIntegerField(default=0, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    validationmethod = models.CharField(max_length= 255, blank=False)

    @property
    def expired(self):
        return timezone.now().date() > self.enddate
    
    def __str__(self):
        return self.name
    
    
class CampaignCompletionInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)  
    location = models.CharField(max_length= 255, default = '#')
    
    class Meta:
        unique_together = ('user', 'campaign')  

    def __str__(self):
        return f"{self.user.fullname} - {self.campaign.name} completed at {self.completed_at}"
    


class Reward(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    startdate = models.DateField(blank=False, null=False)
    enddate = models.DateField(blank=False, null=False)
    pointsrequired = models.PositiveIntegerField(default=0, blank=False, null=False)  
    description = models.TextField(blank=False, null=False)

    @property
    def expired(self):
        return timezone.now().date() > self.enddate

    def __str__(self):
        return self.name
    
    
    
class RewardRedeemInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        unique_together = ('user', 'reward')  

    def __str__(self):
        return f"{self.user.fullname} - {self.reward.name} completed at {self.redeemed_at}"
    
    

            

    
    
    