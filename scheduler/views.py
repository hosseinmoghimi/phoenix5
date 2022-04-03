import json
from django.shortcuts import render
from django.views import View

from scheduler.repo import AppointmentRepo
from scheduler.apps import APP_NAME
from core.views import CoreContext,PageContext
from authentication.repo import ProfileRepo
from scheduler.serializers import AppointmentSerializer
TEMPLATE_ROOT="scheduler/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


# Create your views here.
class HomeView(View):
    def get(self,request,*args, **kwargs):
        return AppointmentsView().get(request=request)

# Create your views here.
class AppointmentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointments=AppointmentRepo(request=request).list(*args, **kwargs)
        context['appointments']=appointments
        appointments_s=json.dumps(AppointmentSerializer(appointments,many=True).data)
        context['appointments_s']=appointments_s
        return render(request,TEMPLATE_ROOT+"appointments.html",context)

class AppointmentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointment=AppointmentRepo(request=request).appointment(*args, **kwargs)
        context['appointment']=appointment
        context.update(PageContext(request=request,page=appointment))
        appointment_s=json.dumps(AppointmentSerializer(appointment).data)
        context['appointment_s']=appointment_s
        return render(request,TEMPLATE_ROOT+"appointment.html",context)