from django.shortcuts import render
from core.views import CoreContext
from django.views import View
from .apps import APP_NAME
from .forms import *
from .repo import GroupRepo,AttendanceRepo,SalaryRepo
from .enums import *
from organization.repo import EmployeeRepo
from .serializers import GroupSerializer,AttendanceSerializer,EmployeeSerializer,SalarySerializer
# from organization.serializers import EmployeeSerializer
import json
from .enums import *
from utility.log import leolog


TEMPLATE_ROOT="salary/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    context['TEMPLATE_ROOT']=TEMPLATE_ROOT
    return context

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)

        return render(request,TEMPLATE_ROOT+"index.html",context)


class GroupsView(View):
    def get(self,request,*args, **kwargs):

        context=getContext(request=request)
        context['expand_groups']=True
        groups=GroupRepo(request=request).list(*args, **kwargs)
        groups_s=json.dumps(GroupSerializer(groups,many=True).data)
        context['groups']=groups
        context['groups_s']=groups_s

        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
            group_type_enums=list(t[0] for t in GroupTypeEnum.choices)
            context['group_type_enums']=group_type_enums
            context['group_type_enums_s']=json.dumps(group_type_enums)
        return render(request,TEMPLATE_ROOT+"groups.html",context)
class EmployeeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee']=employee
        
        salaries=employee.salary_set.all()
        salaries=SalaryRepo(request=request).list(employee_id=employee.id,*args, **kwargs)
        salaries_s=json.dumps(SalarySerializer(salaries,many=True).data)
        context['salaries']=salaries
        context['expand_salaries']=True
        context['salaries_s']=salaries_s
        if request.user.has_perm(APP_NAME+".add_salary"):
            context['add_salary_form']=AddSalaryForm()
            context['MAZAYA']=SalaryRowDirectionEnum.MAZAYA
            context['KOSURAT']=SalaryRowDirectionEnum.KOSURAT

        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
        return render(request,TEMPLATE_ROOT+"employee.html",context)

class GroupView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        group=GroupRepo(request=request).group(*args, **kwargs)
        context['group']=group
        
        employees=group.employees.all()
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees']=employees
        context['expand_employees']=True
        context['employees_s']=employees_s

        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
        return render(request,TEMPLATE_ROOT+"group.html",context)

        
class SalaryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        group=GroupRepo(request=request).group(*args, **kwargs)
        context['group']=group
        
        employees=group.employees.all()
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees']=employees
        context['expand_employees']=True
        context['employees_s']=employees_s

        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
        return render(request,TEMPLATE_ROOT+"group.html",context)