from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from transport.models import Passenger,Driver, Trip, TripCategory, TripPath, Vehicle
from map.serializers import LocationSerializer

class DriverSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Driver
        fields=['id','title','logo','profile','get_absolute_url','balance_rest']
        
class PassengerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Passenger
        fields=['id','title','logo','profile','get_absolute_url','balance_rest']

class TripPathSerializer(serializers.ModelSerializer):
    source=LocationSerializer()
    destination=LocationSerializer()
    class Meta:
        model=TripPath
        fields=['id','destination','source','title','cost','distance','get_absolute_url','duration']

class TripCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripCategory
        fields=['id','title','color','get_absolute_url']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model =Vehicle
        fields=['id','title','plaque','get_absolute_url']


class TripSerializer(serializers.ModelSerializer):
    paths=TripPathSerializer(many=True)
    driver=DriverSerializer()
    passengers=PassengerSerializer(many=True)
    category=TripCategorySerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=Trip
        fields=['id','paths','status','vehicle','passengers','title','cost','distance','driver','get_absolute_url','duration','delay','category']
