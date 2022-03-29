from django import forms

class AddLocationForm(forms.Form):
    title=forms.CharField(max_length=500,required=True)
    location=forms.CharField(max_length=500,required=True)
    page_id=forms.IntegerField(required=False)
               
class AddPageLocationForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    location_id=forms.IntegerField(required=True)
               