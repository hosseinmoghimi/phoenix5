from organization.models import Employee
from core.enums import ParameterNameEnum
from core.repo import PagePermissionRepo, PageRepo, ParameterRepo
from map.repo import LocationRepo
from django.utils import timezone
from utility.calendar import PersianCalendar
from projectmanager.enums import ProjectManagerParameterEnum, RequestStatusEnum, SignatureStatusEnum
from projectmanager.apps import APP_NAME
from projectmanager.models import  Event, Letter,Material, MaterialInvoice, MaterialRequest,Service, Project,OrganizationUnit, Request, RequestSignature, ServiceInvoice, ServiceRequest,WareHouse
from organization.repo import EmployeeRepo,OrganizationUnitRepo
from authentication.repo import ProfileRepo
from django.db.models import Q

from accounting.repo import ServiceRepo,ProductRepo as MaterialRepo
 

class MaterialInvoiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=MaterialInvoice.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def material_invoice(self, *args, **kwargs):
        pk=0
        if 'material_invoice_id' in kwargs:
            pk=kwargs['material_invoice_id']
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
        if 'organization_unit_id' in kwargs:
            objects = objects.filter(pk=0)
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.order_by('date_added') 


class ServiceInvoiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=ServiceInvoice.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def service_invoice(self, *args, **kwargs):
        pk=0
        if 'service_invoice_id' in kwargs:
            pk=kwargs['service_invoice_id']
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
        if 'organization_unit_id' in kwargs:
            objects = objects.filter(pk=0)
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.order_by('date_added') 
 

class ProjectRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        

        show_archive_projects=ParameterRepo(request=self.request,app_name=APP_NAME).parameter(name=ProjectManagerParameterEnum.SHOW_ARCHIVE_PAGES,default="0").boolean_value
        self.objects=Project.objects
        if not show_archive_projects:
            self.objects=self.objects.filter(archive=False)

        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is not None and self.user.is_authenticated and self.user.has_perm(APP_NAME+".view_project"):
            self.objects=self.objects.all()
        elif self.profile is not None:
            me_emp=Employee.objects.filter(account__profile_id=self.profile.id).first()
            if me_emp is not None:

                self.objects=self.objects.filter(id__in=me_emp.my_project_ids())
        else:
                self.objects=self.objects.filter(id__in=[0])


       

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
            objects=PageRepo(request=self.request).list(*args, **kwargs).filter(app_name=APP_NAME).filter(class_name='project')
            ids=[]
            for obje in objects:
                ids.append(obje.id)
            objects=Project.objects.filter(id__in=ids)
            # objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            parent_id=kwargs['parent_id']
            if parent_id==0 or parent_id is None:
                objects=objects.filter(parent_id=None)
            else:
                objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'employee_id' in kwargs:
            employee=EmployeeRepo(request=self.request).employee(*args, **kwargs)
            if employee is not None and employee.organization_unit is not None:
                objects=employee.organization_unit.project_set.all()
        if 'organization_unit_id' in kwargs:
            organization_unit=OrganizationUnitRepo(request=self.request).organization_unit(organization_unit_id=kwargs['organization_unit_id'])
            if organization_unit is not None:
                projects_employed =organization_unit.projects_employed.all()
                projects_contracted =organization_unit.projects_contracted.all()
                org_projects=organization_unit.project_set.all()
                return (projects_employed,projects_contracted,org_projects)
        return objects.all().order_by("-start_date")
    
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
        if 'percentage_completed' in kwargs and kwargs['percentage_completed'] is not None and kwargs['percentage_completed']>0:
            project.percentage_completed=kwargs['percentage_completed']

        if 'parent_id' in kwargs and kwargs['parent_id'] is not None and kwargs['parent_id']>0:
            parent_id=kwargs['parent_id']
            parent=Project.objects.filter(pk=parent_id).first()
            if parent is not None:
                project.parent=parent
                project.contractor=parent.contractor
                project.employer=parent.employer
                
                
        project.start_date=PersianCalendar().date
        if 'start_date' in kwargs and kwargs['start_date'] is not None and not kwargs['start_date']=="":
            start_date=kwargs['start_date']
            if start_date is not None:
                project.start_date=start_date
        
        project.end_date=PersianCalendar().date
        if 'end_date' in kwargs and kwargs['end_date'] is not None and not kwargs['end_date']=="":
            end_date=kwargs['end_date']
            if end_date is not None:
                project.end_date=end_date

        project.save()
        return project

    def edit_project(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_project"):
            return None
        project=self.project(*args, **kwargs)
        if project is not None:
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'start_date' in kwargs:
                project.start_date=kwargs['start_date']
            if 'end_date' in kwargs:
                project.end_date=kwargs['end_date']
            if 'status' in kwargs:
                project.status=kwargs['status']
            if 'contractor_id' in kwargs:
                project.contractor_id=kwargs['contractor_id']
            if 'employer_id' in kwargs:
                project.employer_id=kwargs['employer_id']
            if 'title' in kwargs:
                project.title=kwargs['title']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
                pass
            if 'archive' in kwargs:
                project.archive=kwargs['archive']
            project.save()
            return project


class EventRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        me_employer=EmployeeRepo(request=self.request).me
        
        show_archive_projects=ParameterRepo(request=self.request,app_name=APP_NAME).parameter(name=ProjectManagerParameterEnum.SHOW_ARCHIVE_PAGES,default="0").boolean_value
        self.objects=Event.objects
        if not show_archive_projects:
            self.objects=self.objects.filter(archive=False)


        if self.user is None:
            self.objects=self.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_event"):
            self.objects=self.objects.all()
        elif me_employer is not None:
            if me_employer is not None:
                my_project_ids=me_employer.my_project_ids()
            self.objects = self.objects.filter(project_related_id__in=my_project_ids)
        elif self.profile is not None:
            self.objects=self.objects.filter(id=0)
        else:
            self.objects=self.objects.filter(id=0)


        self.objects=self.objects.order_by('-event_datetime')

    def event(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'event_id' in kwargs:
            return self.objects.filter(pk=kwargs['event_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    
    def add_event(self,*args, **kwargs):
        if 'project_id' in kwargs:
            project_id= kwargs['project_id']
   
        can_write=False
        if self.profile is not None:
            page_permission=PagePermissionRepo(request=self.request).list(page_id=project_id,profile_id=self.profile.id).first()
            if page_permission is not None:
                can_write=page_permission.can_write

        if self.user.has_perm(APP_NAME+".add_event")  :
            pass
        elif can_write:
            pass
        else:
            return
        if 'start_datetime' in kwargs:
            start_datetime=kwargs['start_datetime']
        if 'end_datetime' in kwargs:
            end_datetime=kwargs['end_datetime']
        if 'event_datetime' in kwargs:
            event_datetime=kwargs['event_datetime']
        else:
            from django.utils import timezone
            event_datetime=PersianCalendar().date
        new_event=Event()
        # new_event.creator=ProfileRepo(user=self.user).me
        new_event.event_datetime=event_datetime
        if 'title' in kwargs:
            new_event.title = kwargs['title']
        if 'event_datetime' in kwargs:
            event_datetime = kwargs['event_datetime']
        

        # event_datetime=PersianCalendar().to_gregorian(event_datetime)
        new_event.event_datetime=event_datetime
        new_event.end_datetime=end_datetime
        new_event.start_datetime=start_datetime
        new_event.project_related_id=project_id
        new_event.creator=self.profile
        new_event.save()
        return new_event
 

    def list(self,*args, **kwargs):
        objects=self.objects.all().order_by('-event_datetime')
        if 'project_id' in kwargs:
            objects=self.objects.filter(project_related_id=kwargs['project_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=self.objects.filter(Q(title__contains=search_for))
        return objects

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_project"):
            return None 
        location=LocationRepo(request=self.request,user=self.user).location(*args, **kwargs)
        event=self.event(*args, **kwargs)
        if event is None or location is None:
            return None
        event.locations.add(location)
        event.save()
        return location


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
    def copy_service_requests(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_servicerequest"):
            return None
        project_repo=ProjectRepo(request=self.request)
        source_project=project_repo.project(project_id=kwargs['source_project_id'])
        destination_project=project_repo.project(project_id=kwargs['destination_project_id'])
        if source_project is None or destination_project is None:
            return
        service_requests=ServiceRequest.objects.filter(project_id=source_project.id)

        
        invoice=ServiceInvoice.objects.filter(id=kwargs['invoice_id']).first()
        if invoice is None:
            invoice=ServiceInvoice()
            invoice.pay_from_id=destination_project.contractor.account.id
            invoice.pay_to_id=destination_project.employer.account.id
            invoice.project_id=destination_project.id
            invoice.save()
        

        for service_request in service_requests:
            new_service_request=ServiceRequest()
            new_service_request.project_id=destination_project.id
            new_service_request.invoice_id=invoice.id
            new_service_request.quantity=service_request.quantity
            new_service_request.product_or_service_id=service_request.product_or_service_id
            new_service_request.date_delivered=service_request.date_delivered
            new_service_request.date_requested=service_request.date_requested
            new_service_request.employee_id=service_request.employee_id
            new_service_request.status=service_request.status
            new_service_request.type=service_request.type
            new_service_request.unit_price=service_request.unit_price
            new_service_request.unit_name=service_request.unit_name
            new_service_request.description=service_request.description
            new_service_request.save()
            # for request_signature in service_request.requestsignature_set.all():
            #     new_request_signature=RequestSignature()
            #     new_request_signature.employee_id=request_signature.employee_id
            #     new_request_signature.status=request_signature.status
            #     new_request_signature.description=request_signature.description
            #     new_request_signature.date_added=request_signature.date_added             
            #     new_request_signature.request_id=new_service_request.id             
            #     new_request_signature.save()
            employee=EmployeeRepo(request=self.request).me
            if employee is not None:
                new_request_signature=RequestSignature()
                new_request_signature.employee_id=employee.id
                new_request_signature.status=RequestStatusEnum.REQUESTED
                new_request_signature.description=""
                new_request_signature.request_id=new_service_request.id             
                new_request_signature.save()
        return ServiceRequest.objects.filter(project_id=destination_project.id)

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
        now=timezone.now()
        if 'date_requested' in kwargs:
            new_service_request.date_requested = kwargs['date_requested']
        else:
            new_service_request.date_requested = now

        if 'date_delivered' in kwargs:
            new_service_request.date_delivered = kwargs['date_delivered']
        if 'project_id' in kwargs:
            new_service_request.project_id = kwargs['project_id']
        if 'employee_id' in kwargs:
            employee_id = kwargs['employee_id']
            if not employee_id==0:
                new_service_request.employee_id=employee_id
        if 'service_id' in kwargs:
            if not kwargs['service_id']==0:
                new_service_request.product_or_service_id = kwargs['service_id']

        if 'invoice_id' in kwargs and kwargs['invoice_id'] is not None and kwargs['invoice_id']==-1: 
            new_service_invoice=ServiceInvoice()
            new_service_invoice.project_id = project.id
            new_service_invoice.pay_from=project.contractor.account
            new_service_invoice.pay_to=project.employer.account
            new_service_invoice.save()
            new_service_request.invoice_id = new_service_invoice.id
        if 'invoice_id' in kwargs and kwargs['invoice_id'] is not None and kwargs['invoice_id']>0: 
            new_service_request.invoice_id = kwargs['invoice_id']
        

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
            new_service_request.date_requested = PersianCalendar().date
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
        if 'service_id' in kwargs:
            objects=objects.filter(product_or_service_id=kwargs['service_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()


class RequestSignatureRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = RequestSignature.objects.order_by('date_added')
        return
        if self.user is not None and self.user.has_perm(APP_NAME+".view_warehouse"):
            self.objects = WareHouse.objects.order_by('title')
        elif self.profile is not None:
            self.objects = WareHouse.objects.filter(account__profile=self.profile).order_by('title')
        else:
            self.objects = WareHouse.objects.filter(pk__lte=0).order_by('title')

    def add_signature(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".add_requestsignature"):
            pass
        
        from projectmanager.repo import EmployeeRepo
        employee=EmployeeRepo(request=self.request).me
        if employee is None:
            return
        signature=RequestSignature()
        if 'request_id' in kwargs:
            signature.request_id=kwargs['request_id']
        if 'status' in kwargs:
            signature.status=kwargs['status']
        if 'description' in kwargs:
            signature.description=kwargs['description']
        
        signature.employee_id=employee.id
        signature.save()
        if employee.organization_unit.id==signature.request.project.employer.id or employee.organization_unit.id==signature.request.project.contractor.id:
            signature.request.status=signature.status
            signature.request.save()
        return signature
    
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'employee_id' in kwargs:
            objects= objects.filter(employee_id=kwargs['employee_id'])
        return objects
    
    def request_signature(self, *args, **kwargs):
        if 'request_signature_id' in kwargs:
            return self.objects.filter(pk=kwargs['request_signature_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'store_id' in kwargs:
            return self.objects.filter(store_id=kwargs['store_id']).first()
        if 'owner_id' in kwargs:
            return self.objects.filter(owner_id=kwargs['owner_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
            

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
        now=timezone.now()
        if 'date_requested' in kwargs:
            new_material_request.date_requested = kwargs['date_requested']
        else:
            new_material_request.date_requested = now

        if 'date_delivered' in kwargs:
            new_material_request.date_delivered = kwargs['date_delivered']
        if 'invoice_id' in kwargs and kwargs['invoice_id'] is not None and kwargs['invoice_id']>0: 
            new_material_request.invoice_id = kwargs['invoice_id']
        if 'invoice_id' in kwargs and kwargs['invoice_id'] is not None and kwargs['invoice_id']==-1: 
            new_material_invoice=MaterialInvoice()
            new_material_invoice.project_id = project.id
            # new_material_invoice.invoice_id = kwargs['invoice_id']
            new_material_invoice.pay_from=project.contractor.account
            new_material_invoice.pay_to=project.employer.account
            new_material_invoice.save()
            new_material_request.invoice_id = new_material_invoice.id
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
            new_material_request.date_requested = PersianCalendar().date
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

    def copy_material_requests(self,*args, **kwargs):
        print(10*" kwargs")
        print(kwargs)
        if not self.user.has_perm(APP_NAME+".add_materialrequest"):
            return None
        project_repo=ProjectRepo(request=self.request)
        source_project=project_repo.project(project_id=kwargs['source_project_id'])
        destination_project=project_repo.project(project_id=kwargs['destination_project_id'])
        # print(10*" source_project")
        # print(source_project)
        # print(10*" destination_project")
        # print(destination_project)
        if source_project is None or destination_project is None:
            return 

        invoice=MaterialInvoice.objects.filter(id=kwargs['invoice_id']).first()
        
        
        if invoice is None:
            invoice=MaterialInvoice()
            invoice.pay_from_id=destination_project.contractor.account.id
            invoice.pay_to_id=destination_project.employer.account.id
            invoice.project_id=destination_project.id
            invoice.save()

        # print(10*" invoice")
        # print(invoice)
        
        material_requests=MaterialRequest.objects.filter(project_id=source_project.id)
        for material_request in material_requests:
            new_material_request=MaterialRequest()
            new_material_request.invoice_id=invoice.id
            new_material_request.project_id=destination_project.id
            new_material_request.quantity=material_request.quantity
            new_material_request.product_or_service_id=material_request.product_or_service_id
            new_material_request.date_delivered=material_request.date_delivered
            new_material_request.date_requested=material_request.date_requested
            new_material_request.employee_id=material_request.employee_id
            new_material_request.status=material_request.status
            new_material_request.type=material_request.type
            new_material_request.unit_price=material_request.unit_price
            new_material_request.unit_name=material_request.unit_name
            new_material_request.description=material_request.description
            new_material_request.save()
            # for request_signature in service_request.requestsignature_set.all():
            #     new_request_signature=RequestSignature()
            #     new_request_signature.employee_id=request_signature.employee_id
            #     new_request_signature.status=request_signature.status
            #     new_request_signature.description=request_signature.description
            #     new_request_signature.date_added=request_signature.date_added             
            #     new_request_signature.request_id=new_service_request.id             
            #     new_request_signature.save()
            employee=EmployeeRepo(request=self.request).me
            if employee is not None:
                new_request_signature=RequestSignature()
                new_request_signature.employee_id=employee.id
                new_request_signature.status=RequestStatusEnum.REQUESTED
                new_request_signature.description=""
                new_request_signature.request_id=new_material_request.id             
                new_request_signature.save()
        return MaterialRequest.objects.filter(project_id=destination_project.id)
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
        if 'material_id' in kwargs:
            objects=objects.filter(product_or_service_id=kwargs['material_id'])
        if 'product_id' in kwargs:
            objects=objects.filter(product_or_service_id=kwargs['product_id'])
        if 'project_id' in kwargs:
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()
