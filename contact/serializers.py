from rest_framework import serializers
from .models import Contact
from accounting.serializers import AccountSerializer


class ContactSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Contact
        fields=['id','account','name','value','url','get_edit_url','get_delete_url']
