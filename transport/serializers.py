from lib2to3.pgen2 import driver
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from transport.models import Luggage, Maintenance, Passenger,Driver, ServiceMan, Trip, TripCategory, TripPath, Vehicle,Client, WorkShift
from map.serializers import AreaSerializer, LocationSerializer
from accounting.serializers import AccountSerializer


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model =Vehicle
        fields=['id','title','plaque','thumbnail','brand','vehicle_type','color','get_absolute_url','get_edit_url','get_delete_url']


class LuggageSerializer(serializers.ModelSerializer):
    owner=AccountSerializer()
    class Meta:
        model =Luggage
        fields=['id','title','thumbnail','is_fragile','owner','price','dimension','length','width','height','weight_unit','weight','get_absolute_url','get_edit_url','get_delete_url']




class DriverSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Driver
        fields=['id','title','account','get_absolute_url']
        
class PassengerSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Passenger
        fields=['id','title','account','get_absolute_url']

class ClientSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Client
        fields=['id','title','account','get_absolute_url']

class TripPathSerializer(serializers.ModelSerializer):
    source=LocationSerializer()
    destination=LocationSerializer()
    class Meta:
        model=TripPath
        fields=['id','destination','source','title','cost','distance','get_absolute_url','duration']


 
class WorkShiftSerializer(serializers.ModelSerializer):
    driver=DriverSerializer()
    client=ClientSerializer()
    vehicle=VehicleSerializer()
    area=AreaSerializer()
    class Meta:
        model=WorkShift
        fields=['id','vehicle','client','driver','persian_start_datetime','persian_end_datetime','amount','area','get_absolute_url','get_edit_url']



class ServiceManSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=ServiceMan
        fields=['id','title','account','get_absolute_url']

class MaintenanceSerializer(serializers.ModelSerializer):
    service_man=ServiceManSerializer()
    client=ClientSerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=Maintenance
        fields=['id','maintenance_type','get_edit_url','kilometer','service_man','client','amount','vehicle','get_absolute_url','persian_event_datetime']




class TripCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCategory
        fields=['id','title','count_of_trips','color','get_absolute_url']

class TripSerializer(serializers.ModelSerializer):
    trip_paths=TripPathSerializer(many=True)
    client=ClientSerializer()
    driver=DriverSerializer()
    passengers=PassengerSerializer(many=True)
    trip_category=TripCategorySerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=Trip
        fields=['id','persian_date_started','persian_date_ended','get_edit_url','get_delete_url','trip_paths','client','status','vehicle','passengers','title','cost','distance','driver','get_absolute_url','duration','delay','trip_category']

 