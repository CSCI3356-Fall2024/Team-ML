from django import forms
from .models import User, Campaign, Reward, NewsItem
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
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Edit name here'}),
            'startdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Choose date here'}),
            'enddate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Choose date here'}),
            'pointsreward': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edit points here'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Edit Description here', 'rows': 3}),
            'validationmethod': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose Method here'})
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
    
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'startdate', 'enddate', 'pointsrequired', 'description', 'totalamount', 'userredeemlimit', 'image']
        labels = {
            'name': 'Reward Name',
            'startdate': 'Start Date',
            'enddate': 'End Date',
            'pointsrequired': 'Points Required',
            'description': 'Description',
            'totalamount': 'Total redeem amount limit for all users',
            'userredeemlimit': 'Redeem amount limit for each user',
            'image': 'Reward Image',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'startdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'enddate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pointsrequired': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'totalamount': forms.NumberInput(attrs={'class': 'form-control'}),
            'userredeemlimit': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        startdate = cleaned_data.get('startdate')
        enddate = cleaned_data.get('enddate')

        if enddate and startdate and enddate <= startdate:
            raise ValidationError("End date must be after the start date.")
        return cleaned_data

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['headline', 'photo', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter headline'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter news body', 'rows': 5}),
        }
        