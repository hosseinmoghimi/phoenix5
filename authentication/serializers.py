from .models import MembershipRequest, Profile, ProfileContact
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','name','default','first_name','last_name','mobile','address','email','image','get_absolute_url','bio']

class ProfileContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProfileContact
        fields=['id','name','value','url']

class MembershipRequestSerializer(serializers.ModelSerializer):
    handled_by=ProfileSerializer()
    class Meta:
        model=MembershipRequest
        fields=['id','handled_by','mobile','read','app_name','get_delete_url','handled','persian_date_added','persian_date_handled']
