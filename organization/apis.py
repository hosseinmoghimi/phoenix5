from core.constants import SUCCEED,FAILED
from .forms import *
from django.http import JsonResponse
from organization.repo import EmployeeRepo, LetterRepo, OrganizationUnitRepo
from organization.serializers import EmployeeSerializer, LetterSentSerializer,OrganizationUnitWithEmployeesSerializer, OrganizationUnitSerializer
from rest_framework.views import APIView

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

                
                organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(**fm)
                if organization_unit is not None:
                    context['organization_unit']=OrganizationUnitWithEmployeesSerializer(organization_unit).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        

class AddEmployeeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddEmployeeForm_=AddEmployeeForm(request.POST)
            if AddEmployeeForm_.is_valid():
                log=3
                cd=AddEmployeeForm_.cleaned_data 
                
                employee=EmployeeRepo(request=request).add_employee(**cd)
                if employee is not None:
                    context['employee']=EmployeeSerializer(employee).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        

class SendLetterApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            SendLetterForm_=SendLetterForm(request.POST)
            if SendLetterForm_.is_valid():
                log=3
                cd=SendLetterForm_.cleaned_data 
                
                letter_sent=LetterRepo(request=request).send_letter(**cd)
                if letter_sent is not None:
                    context['letter_sent']=LetterSentSerializer(letter_sent).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
