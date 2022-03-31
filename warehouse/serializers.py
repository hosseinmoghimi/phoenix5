from rest_framework import serializers
from projectmanager.serializers import EmployeeSerializer
from authentication.serializers import ProfileSerializer
from .models import WareHouse,WareHouseSheet, WareHouseSheetSignature
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




class WareHouseSheetSignatureSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model = WareHouseSheetSignature
        fields = ['id','employee', 'get_absolute_url','persian_date_added','description','get_delete_url','get_edit_url']


 