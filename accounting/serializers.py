from rest_framework import serializers
from .models import Account, Asset, Cheque, FinancialBalance, FinancialDocument, Invoice, InvoiceLine, Payment, Price, Product, ProductOrService,Service,  Transaction
from authentication.serializers import ProfileSerializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url','buy_price','available','unit_price','unit_name','thumbnail']

class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url', 'thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'get_absolute_url','buy_price','unit_price','unit_name','thumbnail']

class AccountSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Account
        fields = ['id','logo','class_title','balance_rest', 'title','profile', 'get_absolute_url']


class InvoiceSerializer(serializers.ModelSerializer):
    pay_to = AccountSerializer()
    pay_from = AccountSerializer()
    class Meta:
        model = Invoice
        fields = ['id','pay_to','pay_from', 'title','get_absolute_url']



class ChequeSerializer(serializers.ModelSerializer):
    pay_to=AccountSerializer()
    pay_from=AccountSerializer()
    class Meta:
        model = Cheque
        fields = ['id','title','status','color','pay_to','pay_from','description','amount','get_absolute_url','persian_cheque_date']


class ProductOrServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrService
        fields = ['id', 'title', 'get_absolute_url',
                  'thumbnail']



class InvoiceLineSerializer(serializers.ModelSerializer):
    product_or_service=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','product_or_service','unit_name', 'quantity', 'unit_price',
                  'description','get_absolute_url']

class InvoiceLineWithInvoiceSerializer(serializers.ModelSerializer):
    invoice=InvoiceSerializer()
    product_or_service=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','product_or_service','unit_name', 'quantity', 'unit_price','invoice',
                  'description']



class PaymentSerializer(serializers.ModelSerializer):
    pay_from=AccountSerializer()
    pay_to=AccountSerializer()
    class Meta:
        model = Payment
        fields = ['id','title', 'pay_from','pay_to', 'amount','get_absolute_url','persian_transaction_datetime']



class InvoiceFullSerializer(serializers.ModelSerializer):
    pay_to=AccountSerializer()
    pay_from=AccountSerializer()
    class Meta:
        model = Invoice
        fields = ['id','title','payment_method','status','pay_to','pay_from','description','get_absolute_url','persian_invoice_datetime','ship_fee','discount','tax_percent']

 
class TransactionSerializer(serializers.ModelSerializer):
    pay_to=AccountSerializer()
    pay_from=AccountSerializer()
    class Meta:
        model = Transaction
        fields = ['id','class_title', 'pay_from','pay_to','title','category','persian_transaction_datetime','amount', 'get_absolute_url','payment_method']

class FinancialDocumentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','transaction','get_state_badge', 'account', 'get_absolute_url', 'bedehkar','rest',
                  'bestankar', 'persian_document_datetime', 'get_edit_url','get_delete_url']

 
class PriceSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model = Price
        fields=['id','sell_price','account','unit_name','profit_percentage','buy_price','persian_date_added','get_edit_url','get_delete_url']


class PriceBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields=['id','product_or_service_id','sell_price','unit_name','profit_percentage','buy_price','persian_date_added','get_edit_url','get_delete_url']




class FinancialDocumentForAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','get_state_badge', 'rest','account', 'get_absolute_url', 'bedehkar',
                  'bestankar', 'persian_document_datetime', 'get_edit_url','get_delete_url']



class FinancialBalanceSerializer(serializers.ModelSerializer):
    financial_document = FinancialDocumentSerializer()
    class Meta:
        model = FinancialBalance
        fields = ['id','financial_document','color','bedehkar', 'title', 'bestankar','get_absolute_url','get_delete_url','get_edit_url']


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id','title','thumbnail','get_absolute_url','get_delete_url','get_edit_url']

