from django import forms

class AddContactForm(forms.Form):
    account_id=forms.IntegerField(required=False)
    name=forms.CharField(max_length=50, required=True)
    value=forms.CharField(max_length=50, required=True)
    url=forms.CharField(max_length=50, required=False)