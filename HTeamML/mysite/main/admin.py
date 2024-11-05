from django.contrib import admin

from .models import User, Campaign, CampaignCompletionInfo


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
        'completed_campaigns',  # Make completed_campaigns editable here
    )
    
    readonly_fields = ('id',)  # No need to make completed_campaigns readonly
    
    filter_horizontal = ('completed_campaigns',)  # Adds a horizontal widget for many-to-many fields

    def display_completed_campaigns(self, obj):
        return ", ".join([campaign.name for campaign in obj.completed_campaigns.all()])
    display_completed_campaigns.short_description = 'Completed Campaigns'

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