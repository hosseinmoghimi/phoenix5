from scheduler.models import APP_NAME,Appointment
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from map.serializers import LocationSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    profiles=ProfileSerializer(many=True)
    locations=LocationSerializer(many=True)
    class Meta:
        model=Appointment
        fields=['id','title','profiles','persian_date_fixed','locations','get_absolute_url']
        
