from dataclasses import field
from rest_framework import serializers

from archive.models import Folder
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Folder
        fields=['id','name','get_absolute_url','get_breadcrumb']