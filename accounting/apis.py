import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .enums import WareHouseSheetStatusEnum
from .models import Transaction

from utility.calendar import PersianCalendar
from .repo import ChequeRepo,  FinancialDocumentRepo, InvoiceRepo, TransactionRepo
from django.http import JsonResponse
from .forms import *
from .serializers import ChequeSerializer, FinancialDocumentSerializer

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