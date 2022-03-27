from dataclasses import field
from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    mobile=forms.CharField(max_length=15, required=False)
    class Meta:
        model=User
        fields=['username','password1','password2','mobile','first_name','last_name']
   
class SetDefaultProfileForm(forms.Form):
    profile_id=forms.IntegerField(required=True)

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=50, required=True)
    
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)