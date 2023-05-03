from django import forms
class UpdatePricesForm(forms.Form):
    prices=forms.CharField( max_length=1000, required=True)

class AddMenuForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)