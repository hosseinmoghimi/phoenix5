from django.shortcuts import redirect
from accounting.repo import AccountRepo
from accounting.serializers import AccountSerializer
from core.views import MessageView,PageContext,render,reverse
from accounting.views import get_account_context
from core.views import TEMPLATE_ROOT, CoreContext
from organization.apps import APP_NAME
from organization.forms import *
from django.views import View
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED
import json
from organization.serializers import LetterSerializer,LetterSentSerializer
from organization.repo import EmployeeRepo,OrganizationUnitRepo,LetterRepo
from organization.serializers import EmployeeSerializer,OrganizationUnitSerializer


from projectmanager.repo import ProjectRepo,RequestSignatureRepo
from projectmanager.serializers import ProjectSerializer,RequestSignatureForEmployeeSerializer,ServiceRequestSerializer,MaterialRequestSerializer
from projectmanager.enums import RequestTypeEnum
from projectmanager.views import get_requests_context
from projectmanager.repo import ProjectRepo,RequestSignatureRepo
from utility.log import leolog

LAYOUT_PARENT="phoenix/layout.html"
TEMPLATE_ROOT="organization/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    me_employee=EmployeeRepo(request=request).me
    context['me_employee']=me_employee
    if me_employee is None and not request.user.has_perm(APP_NAME+".view_organizationunit"):
        return None
    return context


def notPersmissionView(request,*args, **kwargs):
        mv=MessageView(request=request)
        mv.body="اکانت شما مجوز دسترسی لازم را دارا نمی باشد."
        mv.title="عدم دسترسی"
        return mv.response()


def get_add_employee_context(request,*args, **kwargs):
    context={}
    context['add_employee_form']=AddEmployeeForm()
    if 'organization_unit' in kwargs:
        organization_units=[kwargs['organization_unit']]
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['new_employee_organization_units']=organization_units
        context['new_employee_organization_units_s']=organization_units_s
    else:
        organization_units=OrganizationUnitRepo(request=request).list()
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['new_employee_organization_units']=organization_units
        context['new_employee_organization_units_s']=organization_units_s


    accounts=AccountRepo(request=request).list()
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['new_employee_accounts']=accounts
    context['new_employee_accounts_s']=accounts_s
    return context


def add_letter_context(request,*args, **kwargs):
    context={}
    # organization_units=OrganizationUnitRepo(request=request).list()
    # organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
    # context['organization_units']=organization_units
    # context['organization_units_s']=organization_units_s
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
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
        if context is None:
            return notPersmissionView(request=request)
        employee = EmployeeRepo(request=request).employee(*args, **kwargs)
        context.update(get_account_context(request=request,account=employee.account))
        context['employee'] = employee
        
        projects = ProjectRepo(request=request).list(employee_id=employee.id)
        context['projects'] = projects
        context['show_all_projects'] = True
        projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
        context['projects_s'] = projects_s

        request_signatures = RequestSignatureRepo(
            request=request).list(employee_id=employee.id)

        context['request_signatures'] = request_signatures
        request_signatures_s = json.dumps(RequestSignatureForEmployeeSerializer(request_signatures, many=True).data)
        context['request_signatures_s'] = request_signatures_s


        # from projectmanager 
        if True:
            context['filter_reauests_form']=True
            requests=employee.request_set
            service_requests=requests.filter(type=RequestTypeEnum.SERVICE_REQUEST)
            context['service_requests'] = request_signatures
            service_requests_s = json.dumps(ServiceRequestSerializer(service_requests, many=True).data)
            context['service_requests_s'] = service_requests_s
            context.update(get_requests_context(request=request))

            material_requests=requests.filter(type=RequestTypeEnum.MATERIAL_REQUEST)
            context['material_requests'] = material_requests
            material_requests_s = json.dumps(MaterialRequestSerializer(material_requests, many=True).data)
            context['material_requests_s'] = material_requests_s

 

        return render(request, TEMPLATE_ROOT+"employee.html", context)


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        context['expand_employees'] = True
        employees = EmployeeRepo(request=request).list(*args, **kwargs)
        context['employees'] = employees
        employees_s = json.dumps(EmployeeSerializer(employees, many=True).data)
        context['employees_s'] = employees_s
        if request.user.has_perm(APP_NAME+".add_employee"):
            context.update(get_add_employee_context(request=request))


        return render(request, TEMPLATE_ROOT+"employees.html", context)


class OrganizationUnitChartView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
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
                names+=(f"""<div style="direction:rtl;"><a href="{employee.get_absolute_url()}"><img src="{employee.account.logo()}" class="rounded-circle" width="48"><small class="text-muted" >{employee.account.title}</small></a></div>""")

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
        if context is None:
            return notPersmissionView(request=request)
        organization_unit = OrganizationUnitRepo(
            request=request).organization_unit(*args, **kwargs)
        if request.user.has_perm("organization.add_letter"):
            context['add_letter_form']=AddLetterForm()
        if organization_unit is None:
            mv=MessageView(request=request)
            mv.title="واحد سازمانی موردنظر یافت نشد."
            mv.body="واحد سازمانی موردنظر یافت نشد."
            return mv.response()
        context.update(PageContext(request=request, page=organization_unit))
        context['organization_unit'] = organization_unit

        for employee in organization_unit.employees:
            if 'profile' in context and context['profile'] is not None and employee.account.profile is not None and employee.account.profile.id==context['profile'].id:
                context['selected_profile']=employee.account.profile

        # employees
        if True:
            employees = EmployeeRepo(request=request).list(
                organization_unit_id=organization_unit.id)
            context['employees_s'] = json.dumps(EmployeeSerializer(employees, many=True).data)
        # add employee
        if True:            
            if request.user.has_perm(APP_NAME+".add_employee"):
                context.update(get_add_employee_context(request=request,organization_unit=organization_unit))

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
            context['accounts']=AccountRepo(request=request).list()
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
            context['show_organization_units_list'] = True

        return render(request, TEMPLATE_ROOT+"organization-unit.html", context)


class OrganizationUnitsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        context['expand_organization_units'] = True
        organization_units = OrganizationUnitRepo(
            request=request).list(parent_id=None, *args, **kwargs)
        context['organization_units'] = organization_units
        organization_units_s = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['organization_units_s'] = organization_units_s
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            
            context['accounts']=AccountRepo(request=request).list()
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
            context['show_organization_units_list'] = True
        return render(request, TEMPLATE_ROOT+"organization-units.html", context)


class LettersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        letters = LetterRepo(request=request).list(*args, **kwargs)
        context['letters'] = letters
        letters_s = json.dumps(LetterSerializer(letters, many=True).data)
        context['letters_s'] = letters_s
        context['expand__letters'] = True
        return render(request, TEMPLATE_ROOT+"letters.html", context)


class LetterPrintView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        letter = LetterRepo(request=request).letter(*args, **kwargs)
        context['letter'] = letter
        context.update(PageContext(request=request, page=letter))
        
        # letter_sents
        if True:
            letter_sents = letter.lettersent_set.all()
            context['letter_sents'] = letter_sents
            letter_sents_s = json.dumps(
                LetterSentSerializer(letter_sents, many=True).data)
            context['letter_sents_s'] = letter_sents_s
        context['no_navbar']=True
        context['no_footer']=True
        return render(request, TEMPLATE_ROOT+"letter-print.html", context)


class LetterView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        letter = LetterRepo(request=request).letter(*args, **kwargs)
        context['letter'] = letter
        context.update(PageContext(request=request, page=letter))
        if True:
            context['send_letter_form']=SendLetterForm()
            
            organization_units=OrganizationUnitRepo(request=request).list()
            organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
            context['organization_units']=organization_units
            context['organization_units_s']=organization_units_s
            
        # letter_sents
        if True:
            letter_sents = letter.lettersent_set.all()
            context['letter_sents'] = letter_sents
            letter_sents_s = json.dumps(
                LetterSentSerializer(letter_sents, many=True).data)
            context['letter_sents_s'] = letter_sents_s

        return render(request, TEMPLATE_ROOT+"letter.html", context)


class AddLetterView(View):
    def post(self, request, *args, **kwargs):
        add_letter_form=AddLetterForm(request.POST)
        if add_letter_form.is_valid():
            cd=add_letter_form.cleaned_data
            letter=LetterRepo(request=request).add_letter(**cd)
            if letter is not None:
                return redirect(letter.get_absolute_url())

    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return notPersmissionView(request=request)
        employee=EmployeeRepo(request=request).me
        if employee is None:
            mv=MessageView(request=request)
            mv.title="خطا در مجوز دسترسی"
            mv.body="شما مجوز لازم برای ایجاد نامه اداری جدید ندارید."
            return mv.response()
        context['expand_add_letter']=True
        context.update(add_letter_context(request=request))
 
        return render(request, TEMPLATE_ROOT+"add-letter.html", context)

