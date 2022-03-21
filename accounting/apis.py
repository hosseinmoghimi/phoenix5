import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .enums import WareHouseSheetStatusEnum
from .models import Transaction

from utility.calendar import PersianCalendar
from .repo import ChequeRepo,  FinancialDocumentRepo, InvoiceRepo, PriceRepo, TransactionRepo
from django.http import JsonResponse
from .forms import *
from .serializers import ChequeSerializer, FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineSerializer, PriceSerializer

class AddChequeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_cheque_form=AddChequeForm(request.POST)



            
            if add_cheque_form.is_valid():
                log=3
                fm=add_cheque_form.cleaned_data
                title=fm['title']
                cheque=ChequeRepo(request=request).add_cheque(
                    title=title,
                )
                if cheque is not None:
                    context['cheque']=ChequeSerializer(cheque).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class EditInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            edit_invoice_form=EditInvoiceForm(request.POST)



            
            if edit_invoice_form.is_valid():
                log=3
                fm=edit_invoice_form.cleaned_data
                lines=fm['lines']
                lines=json.loads(lines)
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                invoice_datetime=fm['invoice_datetime']
                ship_fee=fm['ship_fee']
                tax_percent=fm['tax_percent']
                description=fm['description']
                discount=fm['discount']
                invoice_id=fm['invoice_id']
                payment_method=fm['payment_method']
                status=fm['status']
                invoice_datetime=PersianCalendar().to_gregorian(invoice_datetime)
                invoice=InvoiceRepo(request=request).edit_invoice(
                    invoice_id=invoice_id,
                    lines=lines,
                    status=status,
                    payment_method=payment_method,
                    description=description,
                    discount=discount,
                    pay_from_id=pay_from_id,
                    invoice_datetime=invoice_datetime,
                    pay_to_id=pay_to_id,
                    tax_percent=tax_percent,
                    ship_fee=ship_fee,
                )
                if invoice is not None:
                    context['invoice']=InvoiceFullSerializer(invoice).data
                    context['invoice_lines']=InvoiceLineSerializer(invoice.invoice_lines(),many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
class AddPriceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_price_form=AddPriceForm(request.POST)
            if add_price_form.is_valid():
                log=3
                fm=add_price_form.cleaned_data
                product_or_service_id=fm['product_or_service_id']
                sell_price=fm['sell_price']
                buy_price=fm['buy_price']
                unit_name=fm['unit_name']
                account_id=fm['account_id']
                price=PriceRepo(request=request).add_price(
                    product_or_service_id=product_or_service_id,
                    unit_name=unit_name,
                    account_id=account_id,
                    sell_price=sell_price,
                    buy_price=buy_price,
                )
                if price is not None:
                    context['price']=PriceSerializer(price).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


        