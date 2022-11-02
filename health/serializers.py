
from rest_framework import serializers
from health.models import Disease, Doctor, Drug, Patient, Visit
from health.apps import APP_NAME
from authentication.serializers import ProfileSerializer
from accounting.serializers import AccountSerializer
from core.serializers import DownloadSerializer, PageLinkSerializer

class PatientSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    account=AccountSerializer()
    class Meta:
        model = Patient
        fields=['id','account','get_absolute_url','get_edit_url']

class DoctorSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    account=AccountSerializer()
    class Meta:
        model = Doctor
        fields=['id','account','get_absolute_url','get_edit_url']

class DrugSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    class Meta:
        model = Drug
        fields=['id','title','thumbnail','get_absolute_url','get_edit_url']
class DiseaseSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    class Meta:
        model = Disease
        fields=['id','name','get_absolute_url']

class VisitSerializer(serializers.ModelSerializer):
    diseases=DiseaseSerializer(many=True)
    drugs=DrugSerializer(many=True)
    patient=PatientSerializer()
    doctor=DoctorSerializer()
    class Meta:
        model = Visit
        fields=['id','diseases','drugs','doctor','get_absolute_url','patient','persian_visitdatetime_tag']