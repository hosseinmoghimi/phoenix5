from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from transport.models import Passenger,Driver, TripPath
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
