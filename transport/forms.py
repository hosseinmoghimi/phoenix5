
from django import forms

class AddLuggageForm(forms.Form):
    title=forms.CharField(max_length=100,required=True)
    description=forms.CharField(max_length=1000,required=False)
    weight_unit=forms.CharField(max_length=100,required=False)
    length=forms.IntegerField(required=False)
    width=forms.IntegerField(required=False)
    height=forms.IntegerField(required=False)
    owner_id=forms.IntegerField(required=True)
    weight=forms.IntegerField(required=False)
    price=forms.IntegerField(required=False)

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
    status=forms.CharField(max_length=50, required=False)
    payment_method=forms.CharField(max_length=50, required=False)
    

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
    title=forms.CharField(max_length=200,required=True)
    vehicle_id=forms.IntegerField(required=True)
    area_id=forms.IntegerField(required=True)
    # driver_id=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    pay_to_id=forms.IntegerField(required=True) 
    status=forms.CharField(max_length=50,required=True)
    start_datetime=forms.CharField(max_length=20,required=True)
    end_datetime=forms.CharField(max_length=20,required=True)
    description=forms.CharField(max_length=500,required=False)
