from django import forms
from .models import User, Campaign
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'fullname', 
            'school', 
            'major', 
            'minor', 
            'gradyear'
        ]
        labels = {
            'email': 'Email Address (required)',
            'fullname': 'Full Name (required)',
            'school': 'School (required)',
            'major': 'Major (required)',
            'minor': 'Minor',
            'gradyear': 'Graduation Year (required)'
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'name',
            'startdate',
            'enddate',
            'pointsreward',
            'description',
            'validationmethod'
        ]
        labels = {
            'name': 'New Campaign Name',
            'startdate': 'Start Date',
            'enddate': 'End Date',
            'pointsreward': 'Reward Points',
            'description': 'Campaign Description',
            'validationmethod': 'Validation Method'
        }
        
        widgets = {
            'startdate': forms.DateInput(attrs={'type': 'date'}),
            'enddate': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
        def __init__(self, *args, **kwargs):
            super(CampaignForm, self).__init__(*args, **kwargs)
            
    def clean(self):
        cleaned_data = super().clean()
        startdate = cleaned_data.get('startdate')
        enddate = cleaned_data.get('enddate')

        if enddate and startdate and enddate <= startdate:
            raise ValidationError("Error: End date must be after the start date.")

        if enddate and enddate <= timezone.now().date():
            raise ValidationError("Error: End date must be in the future.")

        return cleaned_data