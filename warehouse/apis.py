import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from warehouse.enums import *

from utility.calendar import PersianCalendar
from .repo import   WareHouseSheetRepo
from django.http import JsonResponse
from .forms import *
from .serializers import WareHouseSheetSerializer
 

class WareHouseSheetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            change_warehouse_sheet_state_form=ChangeWarehouseSheetStateForm(request.POST)

            if change_warehouse_sheet_state_form.is_valid():
                log=33
                fm=change_warehouse_sheet_state_form.cleaned_data
                status=fm['status']
                if status=='DONE':
                    status=WareHouseSheetStatusEnum.DONE
                elif status=='INITIAL':
                    status=WareHouseSheetStatusEnum.INITIAL
                elif status=='IN_PROGRESS':
                    status=WareHouseSheetStatusEnum.IN_PROGRESS
                else:
                    status=WareHouseSheetStatusEnum.INITIAL

                warehouse_sheet_id=fm['warehouse_sheet_id']
                warehouse_sheet=WareHouseSheetRepo(request=request).change_state(
                    warehouse_sheet_id=warehouse_sheet_id,
                    status=status,
                )
                if warehouse_sheet is not None:
                    context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
