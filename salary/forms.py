from django import forms



class AddSalaryForm(forms.Form):
    employee_id=forms.IntegerField(required=False) 
    amount=forms.IntegerField(required=False) 
    month=forms.IntegerField(required=False) 
    year=forms.IntegerField(required=False) 
    direction=forms.CharField(max_length=50, required=False)
    title=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=500, required=False)

class AddGroupForm(forms.Form):
    title=forms.CharField(max_length=100, required=False)
    type=forms.CharField(max_length=100, required=False)
    description=forms.CharField(max_length=500, required=False)