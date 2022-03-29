from rest_framework import serializers
from .models import Location, PageLocation

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','longitude','location','latitude','title','get_absolute_url']


         
class PageLocationSerializer(serializers.ModelSerializer):
    location=LocationSerializer()
    class Meta:
        model=PageLocation
        fields=['id','location','get_edit_url','get_delete_url']


         