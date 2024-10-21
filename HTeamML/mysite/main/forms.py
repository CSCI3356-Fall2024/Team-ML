from django import forms
from .models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'school', 'email', 'major', 'gradyear']
