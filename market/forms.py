from django import forms
class SearchForm(forms.Form):
    searrch_for=forms.CharField(max_length=50, required=True)

    
class AddCategoryFrom(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    parent_id=forms.IntegerField( required=False)
