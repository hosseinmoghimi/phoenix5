from rest_framework import serializers
from .models import Parameter

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','value','get_edit_url','get_delete_url']