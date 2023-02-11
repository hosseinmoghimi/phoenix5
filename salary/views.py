from utility.calendar import to_persian_month_name
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
        if 'month' in kwargs and 'year' in kwargs:
            context['print_employee_year_month']=True
            month=kwargs['month'] 
            year=kwargs['year']
            context['month']=month
            context['year']=year
            month_name=to_persian_month_name(month)
            context['month_name']=month_name
            context['title']=f"""حقوق {employee.account.title} در {month_name} {year}"""
            monthly_salaries=[]
            salaries=SalaryRepo(request=request).list(employee_id=employee.id,month=month,year=year)
        if 'year' in kwargs and not 'month' in kwargs:
            year=kwargs['year'] 
            context['year']=year
            monthly_salaries=[]
            salaries=employee.salary_set.filter(year=year)
            salaries=SalaryRepo(request=request).list(employee_id=employee.id,year=year)

        if 'month' in kwargs or 'year' in kwargs:
            monthly_salaries_s=json.dumps(monthly_salaries)
            context['monthly_salaries_s']=monthly_salaries_s
        else:
            salaries=SalaryRepo(request=request).list(employee_id=employee.id)

        # salaries=SalaryRepo(request=request).list(employee_id=employee.id,*args, **kwargs)
        salaries_s=json.dumps(SalarySerializer(salaries,many=True).data)
        context['salaries']=salaries
        context['expand_salaries']=True
        context['salaries_s']=salaries_s
        
        context['select_salary_form']=SelectSalaryForm()
        
        if request.user.has_perm(APP_NAME+".add_salary") and 'month' in kwargs and 'year' in kwargs:
            context['add_salary_form']=AddSalaryForm()
            context['MAZAYA']=SalaryRowDirectionEnum.MAZAYA
            context['KOSURAT']=SalaryRowDirectionEnum.KOSURAT
            context['SalaryRows']=SalaryRows

        if request.user.has_perm(APP_NAME+".add_group"):
            context['add_group_form']=AddGroupForm()
        return render(request,TEMPLATE_ROOT+"employee.html",context)
    def post(self,request,*args, **kwargs):
        select_salary_form=SelectSalaryForm(request.POST)
        if select_salary_form.is_valid():
            month=select_salary_form.cleaned_data['month']
            employee_id=select_salary_form.cleaned_data['employee_id']
            year=select_salary_form.cleaned_data['year']
            return self.get(request,pk=employee_id,month=month,year=year)

class PrintEmployeeSalaryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee']=employee
        context['no_navbar']=True
        context['no_footer']=True
        if 'month' in kwargs and 'year' in kwargs:
            context['print_employee_year_month']=True
            month=kwargs['month'] 
            year=kwargs['year']
            context['month']=month
            context['year']=year
            month_name=to_persian_month_name(month)
            context['month_name']=month_name
            context['title']=f"""حقوق {employee.account.title} در {month_name} {year}"""
            monthly_salaries=[]
            salaries=SalaryRepo(request=request).list(employee_id=employee.id,month=month,year=year)
        
        # salaries=SalaryRepo(request=request).list(employee_id=employee.id,*args, **kwargs)
        salaries_s=json.dumps(SalarySerializer(salaries,many=True).data)
        context['salaries']=salaries
        mazaya=salaries.filter(direction=SalaryRowDirectionEnum.MAZAYA)
        kosurat=salaries.filter(direction=SalaryRowDirectionEnum.KOSURAT)
         
        context['mazaya']=mazaya
        context['kosurat']=kosurat
        sum_mazaya=0
        sum_kosurat=0

        for maz in mazaya:
            sum_mazaya+=maz.amount
        for kosur in kosurat:
            sum_kosurat+=kosur.amount
        context['sum_total']=sum_mazaya-sum_kosurat
        
        context['sum_mazaya']=sum_mazaya
        context['sum_kosurat']=sum_kosurat
         
        return render(request,TEMPLATE_ROOT+"salary-print.html",context)
  
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