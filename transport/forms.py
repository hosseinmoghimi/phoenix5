
from django import forms
class AddTripForm(forms.Form):
    title=forms.CharField(max_length=50,required=False)
    vehicle_id=forms.IntegerField(required=False)
    passengers=forms.CharField(max_length=500,required=False)
    trip_paths=forms.CharField(max_length=500,required=False)
    pay_from_id=forms.IntegerField(required=False)
    duration=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    delay=forms.IntegerField(required=False)
    pay_to_id=forms.IntegerField(required=False)
    trip_category_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=500,required=False)

class AddWorkShiftForm(forms.Form):
    vehicle_id=forms.IntegerField(required=False)
    driver_id=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    pay_from_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50,required=False)
    pay_to_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=500,required=False)
