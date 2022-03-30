from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import WareHouse,WareHouseSheet
from accounting.serializers import InvoiceLineWithInvoiceSerializer,AccountSerializer
class WareHouseSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model = WareHouse
        fields = ['id', 'title','account', 'get_absolute_url','thumbnail','get_delete_url','get_edit_url']
 

class WareHouseSheetSerializer(serializers.ModelSerializer):
    invoice_line=InvoiceLineWithInvoiceSerializer()
    ware_house=WareHouseSerializer()
    class Meta:
        model = WareHouseSheet
        fields = ['id','quantity','invoice_line','persian_date_registered','unit_name','color', 'ware_house','direction','status', 'get_absolute_url','quantity','get_edit_url']



 