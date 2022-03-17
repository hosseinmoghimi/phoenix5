from urllib import request
from .apps import APP_NAME
from .models import Material,PM_Service as Service, Project,OrganizationUnit,WareHouse

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

         
        if 'parent_id' in kwargs:
            new_organization_unit.parent_id=kwargs['parent_id']
      
      
         
        if 'page_id' in kwargs and kwargs['page_id'] is not None: 
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

   

