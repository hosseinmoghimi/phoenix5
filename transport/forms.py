
from django import forms
class AddTripForm(forms.Form):
    vehicle_id=forms.IntegerField(required=False)
    passengers=forms.CharField(max_length=500,required=False)
    driver_id=forms.IntegerField(required=False)
    pay_to_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=500,required=False)