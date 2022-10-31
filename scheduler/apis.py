from accounting.serializers import AccountSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import FAILED, SUCCEED
from utility.calendar import PersianCalendar
from scheduler.forms import *
from scheduler.repo import AppointmentRepo
from scheduler.serializers import AppointmentSerializer

class AddAppointmentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        add_appointment_form=AddAppointmentForm(request.POST)
        if add_appointment_form.is_valid():
            cd=add_appointment_form.cleaned_data
            datetime_fixed=cd['date_fixed'] 
            datetime_fixed=PersianCalendar().to_gregorian(datetime_fixed)
            cd['date_fixed']=datetime_fixed
            appointment=AppointmentRepo(request=request).add_appointment(**cd)
            if appointment is not None:
                context['result']=SUCCEED
                context['appointment']=AppointmentSerializer(appointment).data
        return JsonResponse(context)

class AddAccountToAppointmentApi(APIView):
    def post(self,request,*args, **kwargs):
        message=""
        result=FAILED
        context={}
        add_appointment_form=AddAccountToAppointmentForm(request.POST)
        if add_appointment_form.is_valid():
            cd=add_appointment_form.cleaned_data
            result,appointment,message=AppointmentRepo(request=request).add_account_to_appointment(**cd)
            if appointment is not None:
                context['accounts']=AccountSerializer(appointment.accounts.all(),many=True).data
        context['message']=message
        context['result']=result
        return JsonResponse(context)
