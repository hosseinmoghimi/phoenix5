from django import forms
class UpdatePricesForm(forms.Form):
    prices=forms.CharField( max_length=1000, required=True)