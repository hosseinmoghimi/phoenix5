from django import forms
from core.forms import SearchForm


class AddPatientForm(forms.Form):
    account_id=forms.IntegerField(required=True)

class AddDoctorForm(forms.Form):
    account_id=forms.IntegerField(required=True)

class AddDrugForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
class AddDiseaseForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)