import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .enums import *

from utility.calendar import PersianCalendar
from .repo import  MaterialRequestRepo, OrganizationUnitRepo, ServiceRequestRepo
from django.http import JsonResponse
from .forms import *
from .serializers import MaterialRequestSerializer, OrganizationUnitSerializer, ServiceRequestSerializer

class AddOrganizationUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddOrganizationUnitForm_=AddOrganizationUnitForm(request.POST)
            if AddOrganizationUnitForm_.is_valid():
                log=3
                fm=AddOrganizationUnitForm_.cleaned_data
                title=fm['title']
                parent_id=fm['parent_id']
                page_id=fm['page_id']
                organization_unit_id=fm['organization_unit_id']
                
                organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(
                    title=title,
                    parent_id=parent_id,
                    organization_unit_id=organization_unit_id,
                    page_id=page_id,
                )
                if organization_unit is not None:
                    context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
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
                    print(material_request)
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
                    print(service_request)
                    context['service_request']=ServiceRequestSerializer(service_request).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        