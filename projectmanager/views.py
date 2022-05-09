
from django.http import JsonResponse
from accounting.repo import InvoiceRepo, PriceRepo
from accounting.serializers import PriceBriefSerializer
from accounting.views import InvoiceView, get_invoice_context, get_service_context, get_product_context,get_account_context
from django.shortcuts import redirect, render
# Create your views here.
from django.shortcuts import render, reverse
from core.constants import FAILED, SUCCEED
from core.enums import UnitNameEnum
from core.views import CoreContext, MessageView, SearchForm, PageContext
# Create your views here.
from django.views import View

from projectmanager.enums import ProjectStatusEnum, SignatureStatusEnum

from .forms import *
from .apps import APP_NAME
# from .repo import MaterialRepo
# from .serializers import MaterialSerializer
import json
from .repo import EventRepo, LetterRepo, MaterialInvoiceRepo, MaterialRepo, MaterialRequestRepo, RequestSignatureRepo, ServiceInvoiceRepo, ServiceRepo, ProjectRepo, ServiceRequestRepo
from .serializers import EventSerializer, LetterSentSerializer, LetterSerializer, MaterialSerializer, ProjectSerializerForGuantt, RequestSignatureForEmployeeSerializer, RequestSignatureSerializer, ServiceSerializer, ProjectSerializer, ServiceRequestSerializer, MaterialRequestSerializer
from organization.repo import EmployeeRepo,OrganizationUnitRepo
from organization.serializers import EmployeeSerializer,OrganizationUnitSerializer
TEMPLATE_ROOT = "projectmanager/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        return render(request, TEMPLATE_ROOT+"index.html", context)


class SearchView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)

        return render(request, TEMPLATE_ROOT+"search.html", context)

    def post(self, request, *args, **kwargs):
        context = getContext(request=request)
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            search_for = cd['search_for']
            context['search_for'] = search_for

            materials = MaterialRepo(request=request).list(
                search_for=search_for)
            context['materials'] = materials
            materials_s = json.dumps(
                MaterialSerializer(materials, many=True).data)
            context['materials_s'] = materials_s

            services = ServiceRepo(request=request).list(search_for=search_for)
            context['services'] = services
            services_s = json.dumps(
                ServiceSerializer(services, many=True).data)
            context['services_s'] = services_s

            events = EventRepo(request=request).list(search_for=search_for)
            context['events'] = events
            events_s = json.dumps(EventSerializer(events, many=True).data)
            context['events_s'] = events_s

            
            organization_units = OrganizationUnitRepo(request=request).list(search_for=search_for)
            context['organization_units'] = organization_units
            organization_units_s = json.dumps(OrganizationUnitSerializer(organization_units, many=True).data)
            context['organization_units_s'] = organization_units_s

            
            projects = ProjectRepo(request=request).list(search_for=search_for)
            context['projects'] = projects
            projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
            context['projects_s'] = projects_s



        return render(request, TEMPLATE_ROOT+"search.html", context)


class ProjectsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        projects = ProjectRepo(request=request).list(*args, **kwargs)
        context['projects'] = projects
        context['show_all_projects'] = True
        projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
        context['projects_s'] = projects_s
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_root_project_form']=AddProjectForm()
            context['statuses']=(i[0] for i in ProjectStatusEnum.choices)
            context['employers']=OrganizationUnitRepo(request=request).list(parent_id=None)
        return render(request, TEMPLATE_ROOT+"projects.html", context)


class LettersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        letters = LetterRepo(request=request).list(*args, **kwargs)
        context['letters'] = letters
        letters_s = json.dumps(LetterSerializer(letters, many=True).data)
        context['letters_s'] = letters_s
        return render(request, TEMPLATE_ROOT+"letters.html", context)


class LetterView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
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

        return render(request, TEMPLATE_ROOT+"letter.html", context)


class RequestView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)

        my_request = MaterialRequestRepo(
            request=request).material_request(*args, **kwargs)
        if my_request is None:
            my_request = ServiceRequestRepo(
                request=request).service_request(*args, **kwargs)

        context['my_request'] = my_request

        request_signatures = my_request.requestsignature_set.all()
        context['request_signatures'] = request_signatures
        request_signatures_s = json.dumps(
            RequestSignatureSerializer(request_signatures, many=True).data)
        context['request_signatures_s'] = request_signatures_s

        # add_signature_form
        if True:
            context['signature_statuses'] = (
                i[0] for i in SignatureStatusEnum.choices)
            employee = EmployeeRepo(request=self.request).me
            if employee is not None:
                context['add_signature_form'] = AddSignatureForm()

        return render(request, TEMPLATE_ROOT+"request.html", context)


class ProjectView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context.update(PageContext(request=request, page=project))

        my_project_ids = []
        me_emp = EmployeeRepo(request=request).me
        if me_emp is not None:
            my_project_ids = me_emp.my_project_ids()

        context['invoices'] = project.invoices()

        events = EventRepo(request=request).list(project_id=project.id)
        context['events'] = events
        events_s = json.dumps(EventSerializer(events, many=True).data)
        context['events_s'] = events_s

        context['project'] = project
        organization_units = OrganizationUnitRepo(request=request).list(
            project_id=project.id, *args, **kwargs)
        context['organization_units'] = organization_units
        organization_units_s = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['organization_units_s'] = organization_units_s

        service_requests = project.service_requests()
        context['service_requests'] = service_requests
        service_requests_s = json.dumps(
            ServiceRequestSerializer(service_requests, many=True).data)
        context['service_requests_s'] = service_requests_s

        material_requests = project.material_requests()
        context['material_requests'] = material_requests
        material_requests_s = json.dumps(
            MaterialRequestSerializer(material_requests, many=True).data)
        context['material_requests_s'] = material_requests_s

        projects = project.childs.order_by('priority')
        projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
        context['project_s'] = json.dumps(ProjectSerializer(project).data)
        context['projects_s'] = projects_s

        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form'] = AddProjectForm()

        if request.user.has_perm(APP_NAME+".change_project") or project.id in my_project_ids:
            employers = OrganizationUnitRepo(request=request).list()
            context['employers'] = employers
            context['employers_s'] = json.dumps(
                OrganizationUnitSerializer(employers, many=True).data)
            context['project_status_enum'] = (i[0]
                                              for i in ProjectStatusEnum.choices)

            context['add_event_form'] = AddEventForm()
            context['edit_project_form'] = EditProjectForm()
            all_organization_units = OrganizationUnitRepo(
                request=request).list()
            context['all_organization_units'] = all_organization_units
            all_organization_units_s = json.dumps(
                OrganizationUnitSerializer(all_organization_units, many=True).data)
            context['all_organization_units_s'] = all_organization_units_s
            context['select_organization_unit_form'] = True
            context['add_service_request_form'] = True
            context['add_material_request_form'] = True
            context['employees_s'] = json.dumps(
                EmployeeSerializer(project.employees(), many=True).data)
            all_service = ServiceRepo(request=request).list()
            context['all_services_s'] = json.dumps(
                ServiceSerializer(all_service, many=True).data)

            context['unit_names'] = (i[0] for i in UnitNameEnum.choices)
            context['unit_names2'] = (i[0] for i in UnitNameEnum.choices)

            if project.contractor.account is not None:
                item_prices = PriceRepo(request=request).list(
                    account_id=project.contractor.account.id)
            else:
                item_prices=[]
            item_prices_s = json.dumps(
                PriceBriefSerializer(item_prices, many=True).data)
            context['item_prices_s'] = item_prices_s

            all_materials = MaterialRepo(request=request).list()
            context['all_materials_s'] = json.dumps(
                MaterialSerializer(all_materials, many=True).data)

        return render(request, TEMPLATE_ROOT+"project.html", context)


class ProjectGuanttView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context['project'] = project
        context['projects_s'] = json.dumps(
            ProjectSerializerForGuantt(project.all_sub_projects().all(), many=True).data)
        return render(request, TEMPLATE_ROOT+"guantt.html", context)


class ProjectChartView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context.update(PageContext(request=request, page=project))

        context['project'] = project
           

        # childs
        if True:
            projects = OrganizationUnitRepo(request=request).list(
                parent_id=project.id, *args, **kwargs)
            context['projects'] = projects 
            
        pages = project.all_sub_projects()

        pages_s=[]
        for page in pages:
            names=""
            pages_s.append({
                'title': f"""{page.title}""",
                'parent_id': page.parent_id,
                'parent': page.parent_id,
                'get_absolute_url': page.get_absolute_url(),
                'id': page.id,
                'sub_title': names,

            })
        for page in [project]:
            names=""
            pages_s.append({
                'title': f"""{page.title}""",
                'parent_id': page.parent_id,
                'parent': page.parent_id,
                'get_absolute_url': page.get_absolute_url(),
                'id': page.id,
                'sub_title': names,

            })
        context['pages_s'] = json.dumps(pages_s)
     



        return render(request, TEMPLATE_ROOT+"project-chart.html", context)


class MaterialInvoiceView(View):

    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        material_invoice = MaterialInvoiceRepo(
            request=request).material_invoice(*args, **kwargs)
        context['material_invoice'] = material_invoice
        if material_invoice is None:
            mv = MessageView(request=request)
            mv.title = "چنین فاکتوری یافت نشد."
            return mv.response()
        context.update(get_invoice_context(request=request,
                       invoice=material_invoice, *args, **kwargs))
        # context['no_navbar'] = True
        # context['no_footer'] = True
        return render(request, TEMPLATE_ROOT+"material-invoice.html", context)


class ServiceInvoiceView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        service_invoice = ServiceInvoiceRepo(
            request=request).service_invoice(*args, **kwargs)
        context['service_invoice'] = service_invoice
        if service_invoice is None:
            mv = MessageView(request=request)
            mv.title = "چنین فاکتوری یافت نشد."
            return mv.response()
        context.update(get_invoice_context(request=request,
                       invoice=service_invoice, *args, **kwargs))
        # context['no_navbar'] = True
        # context['no_footer'] = True
        return render(request, TEMPLATE_ROOT+"service-invoice.html", context)


class MaterialsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        materials = MaterialRepo(request=request).list()
        context['materials'] = materials
        materials_s = json.dumps(MaterialSerializer(materials, many=True).data)
        context['materials_s'] = materials_s
        
        if request.user.has_perm(APP_NAME+".add_material"):
            context['add_material_form']=AddMaterialForm()
        return render(request, TEMPLATE_ROOT+"materials.html", context)


class MaterialView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        material = MaterialRepo(request=request).product(*args, **kwargs)
        context.update(get_product_context(request=request, product=material))
        context['material'] = material

        material_requests = MaterialRequestRepo(request=request).list(material_id=material.id)
        context['material_requests'] = material_requests
        material_requests_s = json.dumps(
            MaterialRequestSerializer(material_requests, many=True).data)
        context['material_requests_s'] = material_requests_s

        return render(request, TEMPLATE_ROOT+"material.html", context)


class ServicesView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        services = ServiceRepo(request=request).list()
        context['services'] = services
        services_s = json.dumps(ServiceSerializer(services, many=True).data)
        context['services_s'] = services_s

        if request.user.has_perm(APP_NAME+".add_service"):
            context['add_service_form']=AddServiceForm()
        return render(request, TEMPLATE_ROOT+"services.html", context)


class ServiceView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)

        service = ServiceRepo(request=request).service(*args, **kwargs)
        context.update(get_service_context(request=request, service=service))

        service_requests = ServiceRequestRepo(request=request).list(service_id=service.id)
        context['service_requests'] = service_requests
        service_requests_s = json.dumps(
            ServiceRequestSerializer(service_requests, many=True).data)
        context['service_requests_s'] = service_requests_s

        return render(request, TEMPLATE_ROOT+"service.html", context)


class EventsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        events = EventRepo(request=request).list()
        context['events'] = events
        events_s = json.dumps(EventSerializer(events, many=True).data)
        context['events_s'] = events_s
        return render(request, TEMPLATE_ROOT+"events.html", context)


class EventView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        event = EventRepo(request=request).event(*args, **kwargs)
        context.update(PageContext(request=request, page=event))
        context['event'] = event
        return render(request, TEMPLATE_ROOT+"event.html", context)
