from django import forms

class AddAppointmentForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    status=forms.CharField(max_length=50, required=True)
    color=forms.CharField(max_length=50, required=True)
    date_fixed=forms.CharField(max_length=30, required=True)
    location_id=forms.IntegerField(required=True)