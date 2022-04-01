from django import forms

class SearchForm(forms.Form):
    searrch_for=forms.CharField(max_length=50, required=False)