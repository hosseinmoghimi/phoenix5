from organization.models import OrganizationUnit,Employee
from core.repo import ParameterRepo
from organization.enums import *
from organization.apps import APP_NAME
from authentication.repo import ProfileRepo

class OrganizationUnitRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=OrganizationUnit.objects 
        show_archive_projects=ParameterRepo(request=self.request,app_name=APP_NAME).parameter(name=OrganizationParameterEnum.SHOW_ARCHIVE_PAGES,default="0").boolean_value
        if not show_archive_projects:
            self.objects=self.objects.filter(archive=False)
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
            from projectmanager.repo import ProjectRepo
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
        if 'project_id' in kwargs:
            from projectmanager.repo import ProjectRepo
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            parent_id=kwargs['parent_id']
            if parent_id==0:
                parent_id=None
            objects=objects.filter(parent_id=parent_id)
        
        return objects.order_by("title") 


class EmployeeRepo():
      
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Employee.objects.order_by("account__title")
        self.profile=ProfileRepo(*args, **kwargs).me
        self.me=Employee.objects.filter(account__profile=self.profile).first()
       
    def employee(self, *args, **kwargs):
        if 'employee_id' in kwargs:
            pk=kwargs['employee_id']
            employee=self.objects.filter(pk=pk).first()
            return employee
        if 'profile_id' in kwargs and kwargs['profile_id'] is not None:
            profile_id=kwargs['profile_id']
            employee=self.objects.filter(pk=profile_id).first()
            if employee is None:
                employee=Employee()
                profile=ProfileRepo(request=self.request).profile(pk=profile_id)

                employee.profile=profile
                employee.save()
                return employee
        if 'account_id' in kwargs and kwargs['account_id'] is not None:
            account_id=kwargs['account_id']
            employee=self.objects.filter(pk=account_id).first()
            if employee is None:
                from accounting.repo import AccountRepo
                employee=Employee()
                account=AccountRepo(request=self.request).account(pk=account_id)
                employee.account_ptr_id=account_id
                employee.profile=account.profile
                employee.save()
                return employee
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            employee=self.objects.filter(pk=pk).first()
            return employee
        elif 'id' in kwargs:
            pk=kwargs['id']
            employee=self.objects.filter(pk=pk).first()
            return employee
     
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
            objects=objects.filter(account__profile_id=kwargs['profile_id'])
        if 'project_id' in kwargs:
            from projectmanager.repo import ProjectRepo
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()

