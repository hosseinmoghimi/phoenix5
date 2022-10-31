from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView

from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import GuaranteeRepo
from django.http import JsonResponse
from .forms import *
from .serializers import GuaranteeSerializer

class AddGuaranteeApi(APIView):
    def post(self,request,*args, **kwargs):
        message=""
        result=FAILED
        context={}
        if request.method=='POST':
            log=2
            AddGuaranteeForm_=AddGuaranteeForm(request.POST)
            if AddGuaranteeForm_.is_valid():
                cd=AddGuaranteeForm_.cleaned_data
                cd['start_date']=PersianCalendar().to_gregorian(cd['start_date'])
                cd['end_date']=PersianCalendar().to_gregorian(cd['end_date'])
                result,message,guarantee=GuaranteeRepo(request=request).add(**cd)
                if result==SUCCEED:
                    context['guarantee']=GuaranteeSerializer(guarantee).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)
