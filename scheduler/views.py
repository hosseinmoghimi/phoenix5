import json
from re import A
from django.shortcuts import render
from django.views import View
from core.enums import ColorEnum
from scheduler.apis import AddAccountToAppointmentApi
from scheduler.enums import *
from scheduler.forms import AddAccountToAppointmentForm, AddAppointmentForm
from scheduler.repo import AppointmentRepo
from scheduler.apps import APP_NAME
from core.views import CoreContext,PageContext
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer

from map.repo import LocationRepo
from accounting.repo import AccountRepo
from accounting.serializers import AccountSerializer

from scheduler.serializers import AppointmentSerializer
TEMPLATE_ROOT="scheduler/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def get_add_appointment_context(request,*args, **kwargs):
    context={}
    profiles=ProfileRepo(request=request).list()
    context['profiles']=profiles
    context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
    
    accounts=AccountRepo(request=request).list()
    context['accounts']=accounts
    context['accounts_s']=json.dumps(AccountSerializer(accounts,many=True).data)
        
    locations=LocationRepo(request=request).list()
    context['locations']=locations


    context['appointment_statuses']=(u[0] for u in AppointmentStatusEnum.choices)
    context['colors']=(u[0] for u in ColorEnum.choices)
    
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
        context['colors_']=(u[0] for u in ColorEnum.choices)
        context['appointment_statuses_']=(u[0] for u in AppointmentStatusEnum.choices)

        context['expand_appointments']=True
        if request.user.has_perm(APP_NAME+".add_appointment"):
            context.update(get_add_appointment_context(request=request))
            context['add_appointment_form']=AddAppointmentForm()
        return render(request,TEMPLATE_ROOT+"appointments.html",context)

class AppointmentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointment=AppointmentRepo(request=request).appointment(*args, **kwargs)
        context['appointment']=appointment
        context.update(PageContext(request=request,page=appointment))
        appointment_s=json.dumps(AppointmentSerializer(appointment).data)
        context['appointment_s']=appointment_s

        accounts=appointment.accounts.all()
        accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
        context['accounts_s']=accounts_s
        context['accounts']=accounts
        if request.user.has_perm(APP_NAME+".change_appointment"):
            context['add_account_to_appointment_form']=AddAccountToAppointmentForm()
            all_accounts=AccountRepo(request=request).list()
            all_accounts_s=json.dumps(AccountSerializer(all_accounts,many=True).data)
            context['all_accounts_s']=all_accounts_s
        return render(request,TEMPLATE_ROOT+"appointment.html",context)