from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from guarantee.models import Guarantee
from accounting.serializers import  InvoiceLineWithInvoiceSerializer
 

class GuaranteeSerializer(serializers.ModelSerializer):
    invoice_line=InvoiceLineWithInvoiceSerializer()
    class Meta:
        model = Guarantee
        fields = ['id', 'invoice_line','type','get_edit_url','status','serial_no','persian_start_date','persian_end_date', 'get_absolute_url']
