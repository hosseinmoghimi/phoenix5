from accounting.apis import AddServiceApi,AddProductApi as AddMaterialApi   
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .enums import *

from utility.calendar import PersianCalendar
from projectmanager.repo import  EventRepo, MaterialRepo, MaterialRequestRepo, ProjectRepo, RequestSignatureRepo, ServiceRepo, ServiceRequestRepo
from django.http import JsonResponse
from organization.repo import OrganizationUnitRepo,EmployeeRepo
from projectmanager.forms import *
from projectmanager.serializers import EventSerializer, MaterialRequestSerializer, MaterialSerializer, OrganizationUnitSerializer, ProjectSerializer, RequestSignatureSerializer, ServiceRequestSerializer, ServiceSerializer


class AddProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddProjectForm_=AddProjectForm(request.POST)
            if AddProjectForm_.is_valid():
                log=3
                fm=AddProjectForm_.cleaned_data
                title=fm['title']
                parent_id=fm['parent_id']
                cd=AddProjectForm_.cleaned_data
                
                if 'start_date' in cd:
                    cd['start_date']=PersianCalendar().to_gregorian(cd['start_date'])
                if 'end_date' in cd:
                    cd['end_date']=PersianCalendar().to_gregorian(cd['end_date'])

                project=ProjectRepo(request=request).add_project(**cd)
                if project is not None:
                    context['project']=ProjectSerializer(project).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
          
class AddSignatureApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddSignatureForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                signature=RequestSignatureRepo(request=request).add_signature(**cd)
                if signature is not None:
                    context['request_signature']=RequestSignatureSerializer(signature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class AddEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_event_form=AddEventForm(request.POST)
            if add_event_form.is_valid():
                log=3
                title=add_event_form.cleaned_data['title']
                event_datetime=add_event_form.cleaned_data['event_datetime']
                start_datetime=add_event_form.cleaned_data['start_datetime']
                end_datetime=add_event_form.cleaned_data['end_datetime']
                project_id=add_event_form.cleaned_data['project_id']
                event_datetime=PersianCalendar().to_gregorian(event_datetime)
                start_datetime=PersianCalendar().to_gregorian(start_datetime)
                end_datetime=PersianCalendar().to_gregorian(end_datetime)
                event=EventRepo(request=request).add_event(start_datetime=start_datetime,end_datetime=end_datetime,event_datetime=event_datetime,project_id=project_id,title=title)
                if event is not None:
                    log=4
                    context['event']=EventSerializer(event).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class EditProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            edit_project_form=EditProjectForm(request.POST)
            if edit_project_form.is_valid():
                cd=edit_project_form.cleaned_data
                archive=cd['archive']
                title=cd['title']
                project_id=cd['project_id']
                percentage_completed=cd['percentage_completed']
                start_date=cd['start_date']
                end_date=cd['end_date']
                status=cd['status']
                employer_id=cd['employer_id']
                weight=cd['weight']
                contractor_id=cd['contractor_id']
                
                start_date=PersianCalendar().to_gregorian(start_date)
                end_date=PersianCalendar().to_gregorian(end_date)
                project=ProjectRepo(request=request).edit_project(weight=weight,title=title,archive=archive,contractor_id=contractor_id,employer_id=employer_id,project_id=project_id,percentage_completed=percentage_completed,start_date=start_date,end_date=end_date,status=status)
                if project is not None: 
                    context['project']=ProjectSerializer(project).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
 
class AddMaterialRequestApi(APIView):
      def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddMaterialRequestForm_=AddMaterialRequestForm(request.POST)
            if AddMaterialRequestForm_.is_valid():
                log=3
                fm=AddMaterialRequestForm_.cleaned_data
                employee_id=fm['employee_id']
                project_id=fm['project_id']
                quantity=fm['quantity']
                unit_name=fm['unit_name']
                unit_price=fm['unit_price']
                material_id=fm['material_id']
                description=fm['description']
                material_request=MaterialRequestRepo(request=request).add_material_request(
                    employee_id=employee_id,
                    project_id=project_id,
                    quantity=quantity,
                    unit_name=unit_name,
                    material_id=material_id,
                    unit_price=unit_price,
                    description=description,
                )
                if material_request is not None:
                    context['material_request']=MaterialRequestSerializer(material_request).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
        
class AddServiceRequestApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddServiceRequestForm_=AddServiceRequestForm(request.POST)
            if AddServiceRequestForm_.is_valid():
                log=3
                fm=AddServiceRequestForm_.cleaned_data
                service_title=fm['service_title']
                employee_id=fm['employee_id']
                project_id=fm['project_id']
                quantity=fm['quantity']
                unit_name=fm['unit_name']
                unit_price=fm['unit_price']
                service_id=fm['service_id']
                description=fm['description']
                service_request=ServiceRequestRepo(request=request).add_service_request(
                    service_title=service_title,
                    employee_id=employee_id,
                    project_id=project_id,
                    quantity=quantity,
                    unit_name=unit_name,
                    service_id=service_id,
                    unit_price=unit_price,
                    description=description,
                )
                if service_request is not None:
                    context['service_request']=ServiceRequestSerializer(service_request).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        