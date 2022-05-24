from django import forms

class AddEmployeeForm(forms.Form):
    job_title=forms.CharField(max_length=50, required=True)
    organization_unit_id=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=True)

class SendLetterForm(forms.Form):
    paraf=forms.CharField(max_length=500, required=True)
    letter_id=forms.IntegerField(required=True)
    recipient_id=forms.IntegerField(required=True)
    
class AddLetterForm(forms.Form):
    title=forms.CharField(max_length=500, required=True)
    employee_id=forms.IntegerField(required=False)

class CreateEmployeeForm(forms.Form):
    profile_id=forms.IntegerField(required=False)
    account_id=forms.IntegerField(required=False)


class AddOrganizationUnitForm(forms.Form):
    page_id=forms.IntegerField( required=False)
    organization_unit_id=forms.IntegerField( required=False)
    account_id=forms.IntegerField(required=False)
    parent_id=forms.IntegerField(required=False)
    is_ware_house=forms.BooleanField(required=False)
    title=forms.CharField(max_length=50, required=False)