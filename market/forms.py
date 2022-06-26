from django import forms
class SearchForm(forms.Form):
    searrch_for=forms.CharField(max_length=50, required=True)

    
class AddCategoryForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    parent_id=forms.IntegerField( required=False)

class AddProductForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    category_id=forms.IntegerField( required=False)
