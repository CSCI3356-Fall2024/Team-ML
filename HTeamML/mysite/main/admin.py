from django.contrib import admin

from .models import User, Campaign, CampaignCompletionInfo, Reward, RewardRedeemInfo


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'fullname', 
        'email', 
        'school', 
        'current_points', 
        'total_points',  
        'supervisor', 
    )
    
    fields = (
        'id', 
        'fullname', 
        'email', 
        'school', 
        'major', 
        'minor', 
        'gradyear', 
        'current_points', 
        'total_points', 
        'profile_completed', 
        'supervisor',
        'completed_campaigns',  
        'redeemed_rewards',
    )
    
    readonly_fields = ('id',)  
    
    filter_horizontal = ('completed_campaigns', 'redeemed_rewards')  

    def display_completed_campaigns(self, obj):
        return ", ".join([campaign.name for campaign in obj.completed_campaigns.all()])
    display_completed_campaigns.short_description = 'Completed Campaigns'
    
    def display_redeemed_rewards(self, obj):
        return ", ".join([reward.name for reward in obj.redeemed_rewards.all()])
    display_redeemed_rewards.short_description = 'Redeemed Rewards'

admin.site.register(User, UserAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'validationmethod')
    
    fields = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'description', 'validationmethod')

    readonly_fields = ('id',)  

admin.site.register(Campaign, CampaignAdmin)


class CampaignCompletionInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'completed_at', 'location')
    list_filter = ('completed_at', 'location', 'campaign')
    search_fields = ('user__fullname', 'campaign__name', 'location')

admin.site.register(CampaignCompletionInfo, CampaignCompletionInfoAdmin)


class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'startdate', 'enddate', 'pointsrequired', 'totalamount', 'userredeemlimit', 'redeemedamount', 'expired')
    
    fields = ('id', 'name', 'startdate', 'enddate', 'pointsrequired', 'description', 'totalamount', 'userredeemlimit', 'redeemedamount', 'expired')

    readonly_fields = ('id', 'expired')  

admin.site.register(Reward, RewardAdmin)


class RewardRedeemInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'redeemed_at')
    list_filter = ('redeemed_at', 'reward')
    search_fields = ('user__fullname', 'reward__name')

admin.site.register(RewardRedeemInfo, RewardRedeemInfoAdmin)