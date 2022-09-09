from django import forms
from core.forms import SearchForm



class AddDrugForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)