from multiprocessing import context
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import FAILED, SUCCEED

from scheduler.forms import *
from scheduler.repo import AppointmentRepo
from scheduler.serializers import AppointmentSerializer

class AddAppointmentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        add_appointment_form=AddAppointmentForm(request.POST)
        if add_appointment_form.is_valid():
            cd=add_appointment_form.cleaned_data
            appointment=AppointmentRepo(request=request).add_appointment(**cd)
            if appointment is not None:
                context['result']=SUCCEED
                context['appointment']=AppointmentSerializer(appointment).data
        return JsonResponse(context)
