from django import forms



class CreateEmployeeForm(forms.Form):
    profile_id=forms.IntegerField(required=False)
    account_id=forms.IntegerField(required=False)


class AddOrganizationUnitForm(forms.Form):
    page_id=forms.IntegerField( required=False)
    organization_unit_id=forms.IntegerField( required=False)
    parent_id=forms.IntegerField(required=False)
    is_ware_house=forms.BooleanField(required=False)
    title=forms.CharField(max_length=50, required=False)