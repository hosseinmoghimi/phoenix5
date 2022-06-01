from django import forms
from core.forms import SearchForm

class AddPropertyForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    address=forms.CharField( max_length=100, required=False)
    area=forms.IntegerField(  required=True)
    agent_id=forms.IntegerField(  required=False)
    price=forms.IntegerField(  required=False)