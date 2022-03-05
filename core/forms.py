from django import forms
class SearchForm(forms.Form):
    app_name=forms.CharField(max_length=50,required=False)
    search_for=forms.CharField(max_length=500,required=True)
class ChangeParameterForm(forms.Form):
    parameter_id=forms.IntegerField(required=False)
    app_name=forms.CharField(max_length=50,required=False)
    parameter_name=forms.CharField(max_length=100,required=False)
    parameter_value=forms.CharField(max_length=10000,required=True)