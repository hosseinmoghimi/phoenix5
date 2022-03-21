from django.utils import timezone
from urllib import request

from projectmanager.enums import RequestStatusEnum, SignatureStatusEnum
from .apps import APP_NAME
from .models import Employee, Material, MaterialRequest,PM_Service as Service, Project,OrganizationUnit, RequestSignature, ServiceRequest,WareHouse

from authentication.repo import ProfileRepo
from django.db.models import Q

class MaterialRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Material.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def material(self, *args, **kwargs):
        pk=0
        if 'material_id' in kwargs:
            pk=kwargs['material_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class ServiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Service.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def service(self, *args, **kwargs):
        pk=0
        if 'service_id' in kwargs:
            pk=kwargs['service_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class ProjectRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Project.objects.order_by("-start_date")
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def project(self, *args, **kwargs):
        pk=0
        if 'project_id' in kwargs:
            pk=kwargs['project_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'organization_unit_id' in kwargs:
            organization_unit=OrganizationUnitRepo(request=self.request).organization_unit(organization_unit_id=kwargs['organization_unit_id'])
            if organization_unit is not None:
                projects_employed =organization_unit.projects_employed.all()
                projects_contracted =organization_unit.projects_contracted.all()
                org_projects=organization_unit.project_set.all()
                return (projects_employed,projects_contracted,org_projects)
        return objects.all()
    
    def add_project(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+'.add_project'):
            return
        project=Project()
        if 'title' in kwargs and kwargs['title'] is not None:
            project.title=kwargs['title']

        if 'contractor_id' in kwargs and kwargs['contractor_id'] is not None and kwargs['contractor_id']>0:
            project.contractor_id=kwargs['contractor_id']

        if 'employer_id' in kwargs and kwargs['employer_id'] is not None and kwargs['employer_id']>0:
            project.employer_id=kwargs['employer_id']

        if 'parent_id' in kwargs and kwargs['parent_id'] is not None and kwargs['parent_id']>0:
            parent_id=kwargs['parent_id']
            parent=Project.objects.filter(pk=parent_id).first()
            if parent is not None:
                project.parent=parent
                project.contractor=parent.contractor
                project.employer=parent.employer
                
                
        project.start_date=timezone.now()
        if 'start_date' in kwargs and kwargs['start_date'] is not None and not kwargs['start_date']=="":
            start_date=kwargs['start_date']
            if start_date is not None:
                project.start_date=start_date
        
        project.end_date=timezone.now()
        if 'end_date' in kwargs and kwargs['end_date'] is not None and not kwargs['end_date']=="":
            end_date=kwargs['end_date']
            if end_date is not None:
                project.end_date=end_date

        project.save()
        return project


class EmployeeRepo():
      
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Employee.objects.order_by("title")
        self.profile=ProfileRepo(*args, **kwargs).me
        self.me=Employee.objects.filter(profile=self.profile).first()
       
    def employee(self, *args, **kwargs):
        pk=0
        if 'employee_id' in kwargs:
            pk=kwargs['employee_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'organization_unit_id' in kwargs:
            objects=objects.filter(organization_unit_id=kwargs['organization_unit_id'])
        if 'profile_id' in kwargs:
            objects=objects.filter(profile_id=kwargs['profile_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()


class ServiceRequestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=ServiceRequest.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_service_request(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_servicerequest"):
            return None
        self.employee=EmployeeRepo(request=self.request).me
        project=ProjectRepo(request=self.request).project(*args, **kwargs)
        if self.employee is not None:
            project=ProjectRepo(request=self.request).project(*args, **kwargs)
            if project is None:
                return


        new_service_request = ServiceRequest(status=RequestStatusEnum.DRAFT)
        if 'project_id' in kwargs:
            new_service_request.project_id = kwargs['project_id']
        if 'employee_id' in kwargs:
            employee_id = kwargs['employee_id']
            if not employee_id==0:
                new_service_request.employee_id=employee_id
        if 'service_id' in kwargs:
            if not kwargs['service_id']==0:
                new_service_request.product_or_service_id = kwargs['service_id']
        if 'quantity' in kwargs:
            new_service_request.quantity = kwargs['quantity']
        if 'unit_name' in kwargs:
            new_service_request.unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            new_service_request.unit_price = kwargs['unit_price']
        if 'description' in kwargs:
            new_service_request.description = kwargs['description']
        if 'status' in kwargs:
            new_service_request.status = kwargs['status']
        if 'date_requested' in kwargs:
            new_service_request.date_requested = kwargs['date_requested']
        else:
            new_service_request.date_requested = timezone.now()
        if 'service_title' in kwargs and not kwargs['service_title']=="":
            service=Service.objects.filter(title=kwargs['service_title']).first()
            if service is None:
                service=Service(title=kwargs['service_title'],unit_price=kwargs['unit_price'],unit_name=kwargs['unit_name'])
                service.save()            
            new_service_request.service_id=service.id
        new_service_request.employee_id = employee_id
        new_service_request.creator=self.employee
        if new_service_request.quantity > 0 and new_service_request.unit_price >= 0:
            new_service_request.save()
            # new_service_request.service.unit_price = new_service_request.unit_price
            # new_service_request.service.unit_name = new_service_request.unit_name
            # new_service_request.service.save()
            if self.employee is not None:
                service_request_signature=RequestSignature(employee=self.employee,request=new_service_request,status=SignatureStatusEnum.REQUESTED)
                service_request_signature.save()
            return new_service_request

    def service_request(self, *args, **kwargs):
        pk=0
        if 'service_request_id' in kwargs:
            pk=kwargs['service_request_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()





class MaterialRequestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=MaterialRequest.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_material_request(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_materialrequest"):
            return None
        self.employee=EmployeeRepo(request=self.request).me
        project=ProjectRepo(request=self.request).project(*args, **kwargs)
        if self.employee is not None:
            project=ProjectRepo(request=self.request).project(*args, **kwargs)
            if project is None:
                return


        new_material_request = MaterialRequest(status=RequestStatusEnum.DRAFT)
        if 'project_id' in kwargs:
            new_material_request.project_id = kwargs['project_id']
        if 'employee_id' in kwargs:
            employee_id = kwargs['employee_id']
            if not employee_id==0:
                new_material_request.employee_id=employee_id
        if 'material_id' in kwargs:
            if not kwargs['material_id']==0:
                new_material_request.product_or_service_id = kwargs['material_id']
        if 'quantity' in kwargs:
            new_material_request.quantity = kwargs['quantity']
        if 'unit_name' in kwargs:
            new_material_request.unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            new_material_request.unit_price = kwargs['unit_price']
        if 'description' in kwargs:
            new_material_request.description = kwargs['description']
        if 'status' in kwargs:
            new_material_request.status = kwargs['status']
        if 'date_requested' in kwargs:
            new_material_request.date_requested = kwargs['date_requested']
        else:
            new_material_request.date_requested = timezone.now()
        if 'material_title' in kwargs and not kwargs['material_title']=="":
            material=Material.objects.filter(title=kwargs['material_title']).first()
            if material is None:
                material=Material(title=kwargs['material_title'],unit_price=kwargs['unit_price'],unit_name=kwargs['unit_name'])
                material.save()            
            new_material_request.material_id=material.id
        new_material_request.employee_id = employee_id
        new_material_request.creator=self.employee
        if new_material_request.quantity > 0 and new_material_request.unit_price >= 0:
            new_material_request.save()
            # new_material_request.material.unit_price = new_material_request.unit_price
            # new_material_request.material.unit_name = new_material_request.unit_name
            # new_material_request.material.save()
            if self.employee is not None:
                material_request_signature=RequestSignature(employee=self.employee,request=new_material_request,status=SignatureStatusEnum.REQUESTED)
                material_request_signature.save()
            return new_material_request

    def material_request(self, *args, **kwargs):
        pk=0
        if 'material_request_id' in kwargs:
            pk=kwargs['material_request_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()





class OrganizationUnitRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=OrganizationUnit.objects.order_by("title")
        self.profile=ProfileRepo(*args, **kwargs).me
       
    def add_organization_unit(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_organizationunit"):
            return None

        if 'organization_unit_id' in kwargs and kwargs['organization_unit_id'] is not None:
            organization_unit=self.organization_unit(pk=kwargs['organization_unit_id'])
            
        if 'is_ware_house' in kwargs and kwargs['is_ware_house']==True:
            new_organization_unit = WareHouse()
        else:
            new_organization_unit = OrganizationUnit()

        if 'title' in kwargs:
            new_organization_unit.title = kwargs['title']

         
        if 'parent_id' in kwargs and kwargs['parent_id'] is not None and kwargs['parent_id']>0:
            new_organization_unit.parent_id=kwargs['parent_id']
      
      
         
        if 'page_id' in kwargs and kwargs['page_id'] is not None : 
            new_organization_unit=organization_unit

            project_id=kwargs['page_id']
            project=ProjectRepo(request=self.request).project(pk=project_id)
            if project is not None:
                project.organization_units.add(organization_unit)
        
      


      
        new_organization_unit.save()
        return new_organization_unit

    def organization_unit(self, *args, **kwargs):
        pk=0
        if 'organization_unit_id' in kwargs:
            pk=kwargs['organization_unit_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()

   

