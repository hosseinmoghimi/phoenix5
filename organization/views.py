from core.views import PageContext
from core.views import MessageView
from django.shortcuts import render
from accounting.views import get_account_context
from core.views import TEMPLATE_ROOT, CoreContext
from organization.apps import APP_NAME
from organization.forms import CreateEmployeeForm,AddOrganizationUnitForm
from django.views import View
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED
from projectmanager.repo import ProjectRepo,RequestSignatureRepo,LetterRepo
import json
from projectmanager.serializers import ProjectSerializer,RequestSignatureForEmployeeSerializer,LetterSerializer
from organization.repo import EmployeeRepo,OrganizationUnitRepo
from organization.serializers import EmployeeSerializer,OrganizationUnitSerializer
LAYOUT_PARENT="phoenix/layout.html"
TEMPLATE_ROOT="organization/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['org']="سنتبالنذبا سیتابسی لبیسغل"
        return render(request,TEMPLATE_ROOT+"index.html",context)



class EmployeeView(View):
    def post(self, request, *args, **kwargs):
        context = {
            'result': FAILED
        }
        create_employee_form = CreateEmployeeForm(request.POST)
        if create_employee_form.is_valid():
            cd = create_employee_form.cleaned_data
            profile_id = cd['profile_id']
            account_id = cd['account_id']
            employee = EmployeeRepo(request=request).employee(
                profile_id=profile_id, account_id=account_id)
            if employee is not None:
                context['employee'] = EmployeeSerializer(employee).data
                context['result'] = SUCCEED

        return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        employee = EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee'] = employee

        projects = ProjectRepo(request=request).list(employee_id=employee.id)
        context['projects'] = projects
        context['show_all_projects'] = True
        projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
        context['projects_s'] = projects_s

        request_signatures = RequestSignatureRepo(
            request=request).list(employee_id=employee.id)

        context['request_signatures'] = request_signatures
        request_signatures_s = json.dumps(
            RequestSignatureForEmployeeSerializer(request_signatures, many=True).data)
        context['request_signatures_s'] = request_signatures_s

        return render(request, TEMPLATE_ROOT+"employee.html", context)


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        employees = EmployeeRepo(request=request).list(*args, **kwargs)
        context['employees'] = employees
        employees_s = json.dumps(EmployeeSerializer(employees, many=True).data)
        context['employees_s'] = employees_s
        return render(request, TEMPLATE_ROOT+"employees.html", context)

class OrganizationUnitChartView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        organization_unit = OrganizationUnitRepo(
            request=request).organization_unit(*args, **kwargs)
        if organization_unit is None:
            mv=MessageView(request=request)
            mv.title="واحد سازمانی موردنظر یافت نشد."
            mv.body="واحد سازمانی موردنظر یافت نشد."
            return mv.response()
        context.update(PageContext(request=request, page=organization_unit))
        context['organization_unit'] = organization_unit

        # employees
        if True:
            employees = EmployeeRepo(request=request).list(
                organization_unit_id=organization_unit.id)
            context['employees_s'] = json.dumps(
                EmployeeSerializer(employees, many=True).data)

     
        # childs
        if True:
            organization_units = OrganizationUnitRepo(request=request).list(
                parent_id=organization_unit.id, *args, **kwargs)
            context['organization_units'] = organization_units
            organization_units_s = json.dumps(
                OrganizationUnitSerializer(organization_units, many=True).data)
            context['organization_units_s'] = organization_units_s
            
        pages = organization_unit.all_sub_orgs()

        pages_s=[]
        for page in pages:
            names=""
            employees=page.employee_set.all()
            for employee in employees:
                names+=(f"""<div style="direction:rtl;"><a href="{employee.get_absolute_url()}"><img src="{employee.account.profile.image}" class="rounded-circle" width="32"><small class="text-muted" >{employee.account.title}</small></a></div>""")
            pages_s.append({
                'title': f"""{page.title}""",
                'parent_id': page.parent_id,
                'parent': page.parent_id,
                'get_absolute_url': page.get_absolute_url(),
                'id': page.id,
                'sub_title': names,

            })
        context['pages_s'] = json.dumps(pages_s)
     
        return render(request, TEMPLATE_ROOT+"organization-unit-chart.html", context)


class OrganizationUnitView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        organization_unit = OrganizationUnitRepo(
            request=request).organization_unit(*args, **kwargs)
        if organization_unit is None:
            mv=MessageView(request=request)
            mv.title="واحد سازمانی موردنظر یافت نشد."
            mv.body="واحد سازمانی موردنظر یافت نشد."
            return mv.response()
        context.update(PageContext(request=request, page=organization_unit))
        context['organization_unit'] = organization_unit

        # employees
        if True:
            employees = EmployeeRepo(request=request).list(
                organization_unit_id=organization_unit.id)
            context['employees_s'] = json.dumps(
                EmployeeSerializer(employees, many=True).data)

        #   letters
        if True:
            letters = LetterRepo(request=request).list(
                organization_unit_id=organization_unit.id)
            # letters=organization_unit.letters.order_by('date_added')
            context['letters'] = letters
            letters_s = json.dumps(LetterSerializer(letters, many=True).data)
            context['letters_s'] = letters_s

        # projects
        if True:
            projects = []
            (projects_employed, projects_contracted, org_projects) = ProjectRepo(
                request=request).list(organization_unit_id=organization_unit.id)
            for project_employed in projects_employed:
                projects.append(project_employed)
            for project_contracted in projects_contracted:
                projects.append(project_contracted)
            for org_project in org_projects:
                projects.append(org_project)
            context['projects'] = projects
            projects_s = json.dumps(
                ProjectSerializer(projects, many=True).data)
            context['projects_s'] = projects_s

        account=organization_unit.account
        if account is not None:
            context['account']=account
            
            context.update(get_account_context(request=request,account=account))
        # childs
        if True:
            organization_units = OrganizationUnitRepo(request=request).list(
                parent_id=organization_unit.id, *args, **kwargs)
            context['organization_units'] = organization_units
            organization_units_s = json.dumps(
                OrganizationUnitSerializer(organization_units, many=True).data)
            context['organization_units_s'] = organization_units_s

        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
            context['show_organization_units_list'] = True

        return render(request, TEMPLATE_ROOT+"organization-unit.html", context)


class OrganizationUnitsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        organization_units = OrganizationUnitRepo(
            request=request).list(parent_id=None, *args, **kwargs)
        context['organization_units'] = organization_units
        organization_units_s = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['organization_units_s'] = organization_units_s
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
            context['show_organization_units_list'] = True
        return render(request, TEMPLATE_ROOT+"organization-units.html", context)

