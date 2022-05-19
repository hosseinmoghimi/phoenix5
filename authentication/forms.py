from dataclasses import field
from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class EditProfileForm(forms.Form):
    # profile_id=forms.IntegerField(required=True)
    first_name=forms.CharField(max_length=100, required=True)
    last_name=forms.CharField(max_length=100, required=True)
    email=forms.CharField(max_length=150, required=False)
    bio=forms.CharField(max_length=150, required=False)
    mobile=forms.CharField(max_length=150, required=False)
    address=forms.CharField(max_length=150, required=False)


class ChangeProfileImageForm(forms.Form):
    profile_id=forms.IntegerField(required=True)
    image=forms.ImageField(required=True)


class AddMembershipRequestForm(forms.Form):
    profile_id=forms.IntegerField(required=True)
    image=forms.ImageField(required=True)

class AddProfileForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=50, required=True)
    email=forms.CharField(max_length=100, required=False)
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)
    bio=forms.CharField(max_length=200, required=False)
    address=forms.CharField(max_length=200, required=False)
    mobile=forms.CharField(max_length=50, required=False)
     



class RegisterForm(UserCreationForm):
    mobile=forms.CharField(max_length=15, required=False)
    class Meta:
        model=User
        fields=['username','password1','password2','mobile','first_name','last_name']
   
class SetDefaultProfileForm(forms.Form):
    profile_id=forms.IntegerField(required=True)

class ResetPasswordForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=100, required=True)
    

class ChangePasswordForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    old_password=forms.CharField(max_length=100, required=True)
    new_password=forms.CharField(max_length=100, required=True)
    
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=50, required=True)
    
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)