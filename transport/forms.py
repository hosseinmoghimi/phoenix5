
from django import forms
class AddTripForm(forms.Form):
    title=forms.CharField(max_length=50,required=False)
    vehicle_id=forms.IntegerField(required=False)
    passengers=forms.CharField(max_length=500,required=False)
    trip_paths=forms.CharField(max_length=500,required=False)
    driver_id=forms.IntegerField(required=False)
    duration=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    delay=forms.IntegerField(required=False)
    client_id=forms.IntegerField(required=False)
    trip_category_id=forms.IntegerField(required=False)
    date_started=forms.CharField(max_length=50,required=False)
    date_ended=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=500,required=False)
    
class AddDriverForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=False)

class AddVehicleForm(forms.Form):
    title=forms.CharField(max_length=100,required=True)
    plaque=forms.CharField(max_length=100,required=True)
    color=forms.CharField(max_length=100,required=False)
    vehicle_type=forms.CharField(max_length=100,required=False)
    brand=forms.CharField(max_length=100,required=False)
    description=forms.CharField(max_length=500,required=False)


class AddMaintenanceForm(forms.Form):
    title=forms.CharField(max_length=100,required=True)
    event_datetime=forms.CharField(max_length=50, required=False)
    maintenance_type=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=500, required=False)
    kilometer=forms.IntegerField( required=False)
    vehicle_id=forms.IntegerField( required=False)
    client_id=forms.IntegerField( required=False)
    service_man_id=forms.IntegerField( required=False)
    amount=forms.IntegerField(required=False)

class AddTripCategoryForm(forms.Form):
    title=forms.CharField(max_length=100,required=True)
    color=forms.CharField(max_length=100,required=True)

class AddTripPathForm(forms.Form):
    source_id=forms.IntegerField(required=True)
    destination_id=forms.IntegerField(required=True)
    duration=forms.IntegerField(required=False)
    distance=forms.IntegerField(required=False)
    area_id=forms.IntegerField(required=False)
    cost=forms.IntegerField(required=False)


class AddPassengerForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=False)

class AddClientForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=False)

class AddServiceManForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=False)

class AddWorkShiftForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    driver_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=False)
    pay_from_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50,required=False)
    pay_to_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=500,required=False)
