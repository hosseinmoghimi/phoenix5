from django import forms

class AddRoleForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=5000, required=False)