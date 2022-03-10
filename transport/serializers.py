from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from transport.models import Passenger,Driver


class DriverSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Driver
        fields=['id','profile','get_absolute_url']
        
class PassengerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Passenger
        fields=['id','profile','get_absolute_url']
