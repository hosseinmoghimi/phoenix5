from rest_framework import serializers
from .models import Account, Cheque, FinancialDocument, Product,Service,  Transaction

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url','buy_price','available','unit_price','unit_name','thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'get_absolute_url','buy_price','unit_price','unit_name','thumbnail']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'title', 'get_absolute_url']




class ChequeSerializer(serializers.ModelSerializer):
    pay_to=AccountSerializer()
    pay_from=AccountSerializer()
    class Meta:
        model = Cheque
        fields = ['id','title','status','color','pay_to','pay_from','description','amount','get_absolute_url','persian_cheque_date']


 
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'title','category', 'get_absolute_url']

class FinancialDocumentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','transaction','get_state_badge', 'account', 'get_absolute_url', 'bedehkar','rest',
                  'bestankar', 'persian_document_datetime', 'get_edit_url','get_delete_url']


class FinancialDocumentForAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','get_state_badge', 'rest','account', 'get_absolute_url', 'bedehkar',
                  'bestankar', 'persian_document_datetime', 'get_edit_url','get_delete_url']

