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
from .serializers import ChequeSerializer, FinancialDocumentSerializer, PriceSerializer

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
                item_id=fm['item_id']
                sell_price=fm['sell_price']
                buy_price=fm['buy_price']
                unit_name=fm['unit_name']
                account_id=fm['account_id']
                price=PriceRepo(request=request).add_price(
                    item_id=item_id,
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


        