
from rest_framework import serializers
from realestate.models import Property
from realestate.apps import APP_NAME
from authentication.serializers import ProfileSerializer
from accounting.serializers import AccountSerializer
from core.serializers import DownloadSerializer, PageLinkSerializer

class PropertySerializer(serializers.ModelSerializer):
    # profile=ProfileSerializer()
    agent=AccountSerializer()
    class Meta:
        model = Property
        fields=['id','title','agent','price','get_absolute_url','get_edit_url']