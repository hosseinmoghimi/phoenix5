
from rest_framework import serializers
from health.models import Drug, Patient
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

class DrugSerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    class Meta:
        model = Drug
        fields=['id','title','thumbnail','get_absolute_url','get_edit_url']