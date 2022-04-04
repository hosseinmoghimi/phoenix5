from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from transport.forms import *
from transport.repo import MaintenanceRepo, WorkShiftRepo
from transport.serializers import WorkShiftSerializer
from django.http import JsonResponse
 

    
class AddMaintenanceApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddMaintenanceForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            work_shift=MaintenanceRepo(request=request).add_maintenance(**cd)
            if work_shift is not None:
                context={
                    'result':SUCCEED,
                    'work_shift':WorkShiftSerializer(work_shift).data
                }
        return JsonResponse(context)

    
class AddWorkShiftApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        fm=AddWorkShiftForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            work_shift=WorkShiftRepo(request=request).add_work_shift(**cd)
            if work_shift is not None:
                context={
                    'result':SUCCEED,
                    'work_shift':WorkShiftSerializer(work_shift).data
                }
        return JsonResponse(context)


