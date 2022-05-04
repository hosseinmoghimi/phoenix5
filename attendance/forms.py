from django import forms



class CreateEmployeeForm(forms.Form):
    profile_id=forms.IntegerField(required=False) 
    delay=forms.IntegerField(required=False) 
    status=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=50, required=False)