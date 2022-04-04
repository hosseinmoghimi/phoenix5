from rest_framework import serializers
from map.models import Area, Location, PageLocation

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','longitude','location','latitude','title','get_absolute_url']


         
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=['id','code','color','area','title','get_absolute_url']


         
class PageLocationSerializer(serializers.ModelSerializer):
    location=LocationSerializer()
    class Meta:
        model=PageLocation
        fields=['id','location','get_edit_url','get_delete_url']


         