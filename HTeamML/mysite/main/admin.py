from django.contrib import admin

from .models import User
from .models import Campaign


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'school', 'major', 'gradyear', 'curent_points', 'total_points', 'profile_completed', 'supervisor')
    fields = ('id', 'fullname', 'email', 'school', 'major', 'minor', 'gradyear', 'curent_points', 'total_points', 'profile_completed', 'supervisor')
    readonly_fields = ('id',)  # Make 'id' read-only to prevent editing

admin.site.register(User, UserAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'validationmethod')
    
    fields = ('id', 'name', 'startdate', 'enddate', 'pointsreward', 'description', 'validationmethod')

    readonly_fields = ('id',)  

admin.site.register(Campaign, CampaignAdmin)