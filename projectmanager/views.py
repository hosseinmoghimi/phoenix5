from accounting.views import get_service_context,get_product_context
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.enums import UnitNameEnum
from core.views import CoreContext,SearchForm,PageContext
# Create your views here.
from django.views import View

from projectmanager.forms import AddOrganizationUnitForm, AddProjectForm
from .apps import APP_NAME
# from .repo import MaterialRepo
# from .serializers import MaterialSerializer
import json
from .repo import EmployeeRepo, MaterialRepo, OrganizationUnitRepo,ServiceRepo,ProjectRepo
from .serializers import EmployeeSerializer, MaterialSerializer, OrganizationUnitSerializer,ServiceSerializer,ProjectSerializer,ServiceRequestSerializer,MaterialRequestSerializer

TEMPLATE_ROOT = "projectmanager/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"index.html",context)


class OrganizationUnitView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        organization_unit=OrganizationUnitRepo(request=request).organization_unit(*args, **kwargs)
        context.update(PageContext(request=request,page=organization_unit))
        context['organization_unit']=organization_unit
        
        employees=EmployeeRepo(request=request).list(organization_unit_id=organization_unit.id)
        context['employees_s']=json.dumps(EmployeeSerializer(employees,many=True).data)
        
        
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form']=AddOrganizationUnitForm()
            context['show_organization_units_list']=True


        projects=[]
        (projects_employed,projects_contracted,org_projects)=ProjectRepo(request=request).list(organization_unit_id=organization_unit.id)
        for project_employed in projects_employed:
            projects.append(project_employed)
        for project_contracted in projects_contracted:
            projects.append(project_contracted)
        for org_project in org_projects:
            projects.append(org_project)

        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s


        organization_units=OrganizationUnitRepo(request=request).list(parent_id=organization_unit.id,*args, **kwargs)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form']=AddOrganizationUnitForm()
            context['show_organization_units_list']=True
        return render(request,TEMPLATE_ROOT+"organization-unit.html",context)


class OrganizationUnitsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        organization_units=OrganizationUnitRepo(request=request).list(parent_id=None,*args, **kwargs)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form']=AddOrganizationUnitForm()
            context['show_organization_units_list']=True
        return render(request,TEMPLATE_ROOT+"organization-units.html",context)


class ProjectsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        projects=ProjectRepo(request=request).list(*args, **kwargs)
        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        return render(request,TEMPLATE_ROOT+"projects.html",context)


class ProjectView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        context.update(PageContext(request=request,page=project))


        context['project']=project  
        organization_units=OrganizationUnitRepo(request=request).list(project_id=project.id,*args, **kwargs)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s


        service_requests=project.service_requests()
        context['service_requests']=service_requests
        service_requests_s=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['service_requests_s']=service_requests_s

        material_requests=project.material_requests()
        context['material_requests']=material_requests
        material_requests_s=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['material_requests_s']=material_requests_s

        projects=project.project_set.order_by('priority')
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s

        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm()

        if request.user.has_perm(APP_NAME+".change_project"):
            all_organization_units=OrganizationUnitRepo(request=request).list()
            context['all_organization_units']=all_organization_units
            all_organization_units_s=json.dumps(OrganizationUnitSerializer(all_organization_units,many=True).data)
            context['all_organization_units_s']=all_organization_units_s
            context['select_organization_unit_form']=True
            context['add_service_request_form']=True
            context['add_material_request_form']=True
            context['employees_s']=json.dumps(EmployeeSerializer(project.employees(),many=True).data)
            all_service=ServiceRepo(request=request).list()
            context['all_services_s']=json.dumps(ServiceSerializer(all_service,many=True).data)

            
            context['unit_names'] = (i[0] for i in UnitNameEnum.choices)
            context['unit_names2'] = (i[0] for i in UnitNameEnum.choices)
            
            all_materials=MaterialRepo(request=request).list()
            context['all_materials_s']=json.dumps(MaterialSerializer(all_materials,many=True).data)

        return render(request,TEMPLATE_ROOT+"project.html",context)



class GuanttChartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        context.update(PageContext(request=request,page=project))


        context['project']=project  
        organization_units=OrganizationUnitRepo(request=request).list(project_id=project.id,*args, **kwargs)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s


        service_requests=project.service_requests()
        context['service_requests']=service_requests
        service_requests_s=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['service_requests_s']=service_requests_s

        material_requests=project.material_requests()
        context['material_requests']=material_requests
        material_requests_s=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['material_requests_s']=material_requests_s

        projects=project.project_set.order_by('priority')
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s

        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm()

        if request.user.has_perm(APP_NAME+".change_project"):
            all_organization_units=OrganizationUnitRepo(request=request).list()
            context['all_organization_units']=all_organization_units
            all_organization_units_s=json.dumps(OrganizationUnitSerializer(all_organization_units,many=True).data)
            context['all_organization_units_s']=all_organization_units_s
            context['select_organization_unit_form']=True
            context['add_service_request_form']=True
            context['add_material_request_form']=True
            context['employees_s']=json.dumps(EmployeeSerializer(project.employees(),many=True).data)
            all_service=ServiceRepo(request=request).list()
            context['all_services_s']=json.dumps(ServiceSerializer(all_service,many=True).data)

            
            context['unit_names'] = (i[0] for i in UnitNameEnum.choices)
            context['unit_names2'] = (i[0] for i in UnitNameEnum.choices)
            
            all_materials=MaterialRepo(request=request).list()
            context['all_materials_s']=json.dumps(MaterialSerializer(all_materials,many=True).data)

        return render(request,TEMPLATE_ROOT+"project.html",context)


class ProjectChartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        context.update(PageContext(request=request,page=project))


        context['project']=project  
        organization_units=OrganizationUnitRepo(request=request).list(project_id=project.id,*args, **kwargs)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s


        service_requests=project.service_requests()
        context['service_requests']=service_requests
        service_requests_s=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['service_requests_s']=service_requests_s

        material_requests=project.material_requests()
        context['material_requests']=material_requests
        material_requests_s=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['material_requests_s']=material_requests_s

        projects=project.project_set.order_by('priority')
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm()

        if request.user.has_perm(APP_NAME+".change_project"):
            all_organization_units=OrganizationUnitRepo(request=request).list()
            context['all_organization_units']=all_organization_units
            all_organization_units_s=json.dumps(OrganizationUnitSerializer(all_organization_units,many=True).data)
            context['all_organization_units_s']=all_organization_units_s
            context['select_organization_unit_form']=True
            context['add_service_request_form']=True
            context['add_material_request_form']=True
            context['employees_s']=json.dumps(EmployeeSerializer(project.employees(),many=True).data)
            all_service=ServiceRepo(request=request).list()
            context['all_services_s']=json.dumps(ServiceSerializer(all_service,many=True).data)

            
            context['unit_names'] = (i[0] for i in UnitNameEnum.choices)
            context['unit_names2'] = (i[0] for i in UnitNameEnum.choices)
            
            all_materials=MaterialRepo(request=request).list()
            context['all_materials_s']=json.dumps(MaterialSerializer(all_materials,many=True).data)

        return render(request,TEMPLATE_ROOT+"project.html",context)


class MaterialsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"materials.html",context)


class MaterialView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        material=MaterialRepo(request=request).material(*args, **kwargs)
        context.update(get_product_context(request=request,product=material))
        context['material']=material
 
        material_requests=material.material_requests()
        context['material_requests']=material_requests
        material_requests_s=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['material_requests_s']=material_requests_s


        return render(request,TEMPLATE_ROOT+"material.html",context)


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        return render(request,TEMPLATE_ROOT+"services.html",context)


class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        service=ServiceRepo(request=request).service(*args, **kwargs)
        context.update(get_service_context(request=request,service=service))
        

        service_requests=service.service_requests()
        context['service_requests']=service_requests
        service_requests_s=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['service_requests_s']=service_requests_s
 

        return render(request,TEMPLATE_ROOT+"service.html",context)
        