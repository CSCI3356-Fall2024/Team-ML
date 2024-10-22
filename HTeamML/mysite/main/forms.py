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