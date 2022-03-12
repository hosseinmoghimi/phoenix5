from rest_framework import serializers
from .models import PageDownload, Parameter,PageLink
from authentication.serializers import ProfileSerializer


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','value','get_edit_url','get_delete_url']



class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageLink
        fields=['id','title','url','get_edit_url','get_delete_url']



class PageDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageDownload
        fields=['id','title','get_edit_url','get_delete_url','get_download_url']


