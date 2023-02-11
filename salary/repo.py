from utility.log import leolog
from salary.models import Group,Attendance,Salary
from core.repo import ParameterRepo
from salary.enums import *
from salary.apps import APP_NAME
from authentication.repo import ProfileRepo
from core.constants import FAILED,SUCCEED

class SalaryRepo():
      
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Salary.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        self.me=Attendance.objects.filter(account__profile=self.profile).first()
       
    def add_salary(self,*args, **kwargs):
        result,message,salary=FAILED,"",None
        if not self.user.has_perm(APP_NAME+".add_salary"):
            return None
            
        salary=Salary(*args, **kwargs)
        # if 'title' in kwargs:
        #     salary.title = kwargs['title']
        # if 'type' in kwargs:
        #     group.type = kwargs['type']
        
        # group.creator=ProfileRepo(request=self.request).me
        salary_old=Salary.objects.filter(employee_id=salary.employee_id).filter(title=salary.title).filter(year=salary.year).filter(month=salary.month)
        
        if len(salary_old)>0:
            message="ردیف حقوقی تکراری"
            return result,message,salary
        salary.save()
        result=SUCCEED
        message="با موفقیت اضافه شد."
        return result,message,salary

    def salary(self, *args, **kwargs):
        if 'salary_id' in kwargs:
            pk=kwargs['salary_id']
            salary=self.objects.filter(pk=pk).first()
            return salary
        if 'salary' in kwargs:
            salary=kwargs['salary']
            return salary
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            salary=self.objects.filter(pk=pk).first()
            return salary
        elif 'id' in kwargs:
            pk=kwargs['id']
            salary=self.objects.filter(pk=pk).first()
            return salary
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'employee_id' in kwargs:
            objects=objects.filter(employee_id=kwargs['employee_id'])
        if 'month' in kwargs:
            objects=objects.filter(month=kwargs['month'])
        if 'year' in kwargs:
            objects=objects.filter(year=kwargs['year'])
        if 'organization_unit_id' in kwargs:
            objects=objects.filter(organization_unit_id=kwargs['organization_unit_id'])
        if 'profile_id' in kwargs:
            objects=objects.filter(account__profile_id=kwargs['profile_id'])
        if 'project_id' in kwargs:
            from projectmanager.repo import ProjectRepo
            project=ProjectRepo(request=self.request).project(project_id=kwargs['project_id'])
            objects=project.organization_units.all()
        return objects.all()


class AttendanceRepo():
      
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Attendance.objects.order_by("account__title")
        self.profile=ProfileRepo(*args, **kwargs).me
        self.me=Attendance.objects.filter(account__profile=self.profile).first()
       
    def attendance(self, *args, **kwargs):
        if 'attendance_id' in kwargs:
            pk=kwargs['attendance_id']
            attendance=self.objects.filter(pk=pk).first()
            return attendance
        if 'attendance' in kwargs:
            attendance=kwargs['attendance']
            return attendance
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


class GroupRepo():
      
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Group.objects.order_by("title")
        self.profile=ProfileRepo(*args, **kwargs).me
       
    def group(self, *args, **kwargs):
        if 'group_id' in kwargs:
            pk=kwargs['group_id']
            group=self.objects.filter(pk=pk).first()
            return group
        if 'group' in kwargs:
            group=kwargs['group']
            return group
         
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

    def add_group(self,*args, **kwargs):
        result,message,group=FAILED,"",None
        if not self.user.has_perm(APP_NAME+".add_group"):
            return None
        if len(Group.objects.filter(title=kwargs['title']))>0:
            message="گروه تکراری "
            return result,message,group
            
        group=Group()
        if 'title' in kwargs:
            group.title = kwargs['title']
        if 'type' in kwargs:
            group.type = kwargs['type']
        
        group.creator=ProfileRepo(request=self.request).me
        group.save()
        result=SUCCEED
        return result,message,group
