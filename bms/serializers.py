from rest_framework import serializers
from bms.models import Feeder,Relay,Command

class FeederSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feeder
        fields=['id','name','get_absolute_url']
        
class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model=Relay
        fields=['id','name','get_absolute_url']
        
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Command
        fields=['id','name','color','get_absolute_url']

class RelayFullSerializer(serializers.ModelSerializer):
    commands=CommandSerializer(many=True)
    class Meta:
        model=Relay
        fields=['id','commands','name','get_absolute_url']

class FeederFullSerializer(serializers.ModelSerializer):
    relays=RelayFullSerializer(many=True)
    class Meta:
        model=Feeder
        fields=['id','name','relays','get_absolute_url']