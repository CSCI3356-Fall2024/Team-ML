from django import forms
from .models import User, Campaign

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
            