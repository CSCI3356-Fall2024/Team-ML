from django.contrib import admin

from .models import User, Campaign


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
        'display_completed_campaigns',
    )
    readonly_fields = ('id', 'display_completed_campaigns',)
    
    def display_completed_campaigns(self, obj):
        return ",  ".join([campaign.name for campaign in obj.completed_campaigns.all()])
    display_completed_campaigns.short_description = 'Completed Campaigns'

admin.site.register(User, UserAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'validationmethod')
    
    fields = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'description', 'validationmethod')

    readonly_fields = ('id',)  

admin.site.register(Campaign, CampaignAdmin)