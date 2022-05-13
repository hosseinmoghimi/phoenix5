from django import forms
class DateTimeForm(forms.Form):
    gregorian_datetime=forms.CharField(max_length=20, required=False)
    persian_datetime=forms.CharField(max_length=20, required=False)