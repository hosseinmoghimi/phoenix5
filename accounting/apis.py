import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .models import Transaction

from utility.calendar import PersianCalendar
from .repo import AccountRepo, ChequeRepo, CostRepo, FinancialBalanceRepo,  FinancialDocumentRepo, InvoiceRepo, PaymentRepo, PriceRepo, ProductRepo, ServiceRepo, TransactionRepo
from django.http import JsonResponse
from .forms import *
from .serializers import AccountSerializer, ChequeSerializer, CostSerializer, FinancialBalanceSerializer, FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineSerializer, PaymentSerializer, PriceSerializer, ProductSerializer, ServiceSerializer

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


class AddCostApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddCostForm_=AddCostForm(request.POST)
            if AddCostForm_.is_valid():
                log=3
                fm=AddCostForm_.cleaned_data
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                
                payment_datetime=fm['payment_datetime']
                description=fm['description']
                amount=fm['amount']
                payment_method=fm['payment_method']
                title=fm['title']
                payment_datetime=PersianCalendar().to_gregorian(payment_datetime)
                cost=CostRepo(request=request).add_cost(
                    payment_method=payment_method,
                    description=description,
                    pay_from_id=pay_from_id,
                    amount=amount,
                    payment_datetime=payment_datetime,
                    pay_to_id=pay_to_id,
                    title=title,
                )
                if cost is not None:
                    context['cost']=CostSerializer(cost).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
        
class AddPaymentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddPaymentForm_=AddPaymentForm(request.POST)
            if AddPaymentForm_.is_valid():
                log=3
                fm=AddPaymentForm_.cleaned_data
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                
                payment_datetime=fm['payment_datetime']
                description=fm['description']
                amount=fm['amount']
                payment_method=fm['payment_method']
                title=fm['title']
                payment_datetime=PersianCalendar().to_gregorian(payment_datetime)
                payment=PaymentRepo(request=request).add_payment(
                    payment_method=payment_method,
                    description=description,
                    pay_from_id=pay_from_id,
                    amount=amount,
                    payment_datetime=payment_datetime,
                    pay_to_id=pay_to_id,
                    title=title,
                )
                if payment is not None:
                    context['payment']=PaymentSerializer(payment).data
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

     
class AddFinancialBalancesApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddFinancialBalanceForm(request.POST)
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
                financial_balances=FinancialBalanceRepo(request=request).add_financial_balance(**cd)
                if financial_balances is not None:
                    context['financial_balances']=FinancialBalanceSerializer(financial_balances,many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
  
     
class AddAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            print(request.POST)
            add_account_form=AddAccountForm(request.POST)
            if add_account_form.is_valid():
                log=333
                cd=add_account_form.cleaned_data
                account=AccountRepo(request=request).add_account(**cd)
                if account is not None:
                    context['account']=AccountSerializer(account).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

     
class AddProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddProductForm(request.POST)
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                product=ProductRepo(request=request).add_product(**cd)
                if product is not None:
                    context['product']=ProductSerializer(product).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    
class AddServiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddServiceForm(request.POST)
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                service=ServiceRepo(request=request).add_service(**cd)
                if service is not None:
                    context['service']=ServiceSerializer(service).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


        