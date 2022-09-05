
from django.http import JsonResponse
from accounting.repo import InvoiceRepo, PriceRepo
from accounting.serializers import InvoiceSerializer, PriceBriefSerializer
from accounting.views import InvoiceView, get_invoice_context, get_service_context, get_product_context,get_account_context
from django.shortcuts import redirect, render
# Create your views here.
from django.shortcuts import render, reverse
from core.constants import FAILED, SUCCEED
from core.enums import UnitNameEnum
from core.repo import PageLikeRepo, PageRepo
from core.serializers import PageSerializer
from core.views import CoreContext, MessageView, SearchForm, PageContext
# Create your views here.
from django.views import View

from projectmanager.enums import ProjectStatusEnum, RequestStatusEnum, SignatureStatusEnum

from .forms import *
from .apps import APP_NAME
# from .repo import MaterialRepo
# from .serializers import MaterialSerializer
import json
from projectmanager.repo import EventRepo, MaterialInvoiceRepo, MaterialRepo, MaterialRequestRepo, RequestSignatureRepo, ServiceInvoiceRepo, ServiceRepo, ProjectRepo, ServiceRequestRepo
from projectmanager.serializers import EventSerializer,  MaterialSerializer, ProjectSerializerForGuantt, RequestSignatureForEmployeeSerializer, RequestSignatureSerializer, ServiceSerializer, ProjectSerializer, ServiceRequestSerializer, MaterialRequestSerializer
from organization.repo import EmployeeRepo,OrganizationUnitRepo
from organization.serializers import EmployeeSerializer,OrganizationUnitSerializer
from accounting.views import getInvoiceLineContext
TEMPLATE_ROOT = "projectmanager/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context
def get_requests_context(request, *args, **kwargs):
    context={}
    context['request_statuses']=(request_status[0] for request_status in RequestStatusEnum.choices)
    context['request_statuses_']=context['request_statuses']
    return context
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        # pages=PageLikeRepo(request=request).list(page__app_name=APP_NAME,profile=)
        # context['pages_s']=json.dumps(PageSerializer(pages,many=True).data)
        me=context['profile']
        if me is not None:
            page_likes=PageLikeRepo(request=request,app_name=APP_NAME).list(profile_id=me.id)
            context['page_likes']=page_likes

        context['expand_likes']=True
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
            context['expand_materials']=True
            
            services = ServiceRepo(request=request).list(search_for=search_for)
            context['services'] = services
            services_s = json.dumps(
                ServiceSerializer(services, many=True).data)
            context['services_s'] = services_s
            context['expand_services']=True

            events = EventRepo(request=request).list(search_for=search_for)
            context['events'] = events
            events_s = json.dumps(EventSerializer(events, many=True).data)
            context['events_s'] = events_s
            context['expand_events']=True


            
            organization_units = OrganizationUnitRepo(request=request).list(search_for=search_for)
            context['organization_units'] = organization_units
            organization_units_s = json.dumps(OrganizationUnitSerializer(organization_units, many=True).data)
            context['organization_units_s'] = organization_units_s
            context['expand_organization_units']=True

            
            projects = ProjectRepo(request=request).list(search_for=search_for)
            context['projects'] = projects
            projects_s = json.dumps(ProjectSerializer(projects, many=True).data)
            context['projects_s'] = projects_s
            context['expand_projects']=True

            pages = PageRepo(request=request).list(search_for=search_for).filter(app_name=APP_NAME)
            context['pages'] = pages
            pages_s = json.dumps(PageSerializer(pages, many=True).data)
            context['pages_s'] = pages_s
            context['expand_pages']=True



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


class ProjectView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        if project is None:
            mv=MessageView(request=request)
            mv.title="پروژه مورد نظر پیدا نشد."
            mv.body="پروژه مورد نظر پیدا نشد."
            return mv.response()
        context.update(PageContext(request=request, page=project))

        my_project_ids = []
        me_emp = EmployeeRepo(request=request).me
        if me_emp is not None:
            my_project_ids = me_emp.my_project_ids()

        context['invoices'] = project.invoices()
        material_invoices=project.materialinvoice_set.all()
        context['material_invoices']=material_invoices
        material_invoices_s=json.dumps(InvoiceSerializer(material_invoices,many=True).data)
        context['material_invoices_s'] = material_invoices_s

        

        invoices = project.invoices()
        context['invoices'] = invoices
        context['invoices_s']=json.dumps(InvoiceSerializer(invoices,many=True).data)

        service_invoices=project.serviceinvoice_set.all()
        context['service_invoices']=service_invoices
        service_invoices_s=json.dumps(InvoiceSerializer(service_invoices,many=True).data)
        context['service_invoices_s'] = service_invoices_s

        

        events = EventRepo(request=request).list(project_id=project.id).order_by('event_datetime')
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

        service_requests = project.service_requests().order_by('invoice_id').order_by('row')
        context['service_requests'] = service_requests
        service_requests_s = json.dumps(
            ServiceRequestSerializer(service_requests, many=True).data)
        context['service_requests_s'] = service_requests_s

        material_requests = project.material_requests().order_by('invoice_id').order_by('row')
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
            statuses=[]
            for status in RequestStatusEnum.choices:
                statuses.append(status[0])
            
            context['statuses_s']=json.dumps(statuses)
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
        context.update(get_requests_context(request=request))



        childs=project.childs.all()
        if len(childs)>0:
            sub_projects_material_requests=project.sub_projects_material_requests()
            if len(sub_projects_material_requests)>0:
                context['sub_projects_material_requests_s']=json.dumps(MaterialRequestSerializer(sub_projects_material_requests,many=True).data)
            sub_projects_service_requests=project.sub_projects_service_requests()
            if len(sub_projects_service_requests)>0:
                context['sub_projects_service_requests_s']=json.dumps(ServiceRequestSerializer(sub_projects_service_requests,many=True).data)



        return render(request, TEMPLATE_ROOT+"project.html", context)


class RequestView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        context.update(getInvoiceLineContext(request=request,*args, **kwargs))

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


class ProjectsListView(View):
    def get(self, request, *args, **kwargs):
        return ProjectsView().get(request=request,parent_id=0,*args, **kwargs)
        # return ProjectsView().get(request=request,*args, **kwargs)


class CopyProjectView(View):
    def post(self, request, *args, **kwargs):
        context = {}
        context['result']=FAILED
        copy_project_form=CopyProjectForm(request.POST)
        if copy_project_form.is_valid():
            project_id=copy_project_form.cleaned_data['project_id']
            project_repo=ProjectRepo(request=request)
            source_project=project_repo.project(pk=project_id)
            if source_project is None:
                message="چنین پروژه ای پیدا نشد."
                mv=MessageView(request=request)
                mv.title=message
                mv.body=message
                return mv.response()
            # project=project_repo.add_project(title=)
        return JsonResponse(context)


class ProjectGuanttView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context['project'] = project
        projects=ProjectRepo(request=request).list(parent_id=project.pk)
        context['projects'] = projects
        context['projects_s'] = json.dumps(ProjectSerializerForGuantt(projects, many=True).data)
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
            names=page.get_full_description_for_chart()
            pages_s.append({
                'title': f"""{page.title}""",
                'parent_id': page.parent_id,
                'parent': page.parent_id,
                'get_absolute_url': page.get_absolute_url(),
                'id': page.id,
                'sub_title': names,

            })
        for page in [project]:
            names=page.get_full_description_for_chart()
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
