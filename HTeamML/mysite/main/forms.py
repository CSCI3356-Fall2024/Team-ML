from django import forms
from .models import User

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
            'email': 'Email Address',
            'fullname': 'Full Name',
            'school': 'School',
            'major': 'Major',
            'minor': 'Minor',
            'gradyear': 'Graduation Year'
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True