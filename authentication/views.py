from django.shortcuts import redirect, render
import json
from core.enums import ParameterNameEnum
from .forms import *
from core.repo import ParameterRepo
from .repo import ProfileRepo
from core.views import CoreContext
from django.views import View
from .apps import APP_NAME
TEMPLATE_ROOT="authentication/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['TEMPLATE_ROOT']=TEMPLATE_ROOT
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    context['title']="auth"
    return context
    

class BasicViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profiles=ProfileRepo(request=request).list()
        context['profiles']=profiles
        return render(request,TEMPLATE_ROOT+"index.html",context)


class ProfileViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        selected_profile=ProfileRepo(request=request).me
        if 'pk' in kwargs:
            selected_profile=ProfileRepo(request=request).profile(*args, **kwargs)
        context['selected_profile']=selected_profile
        
        if True:
            from accounting.views import AccountRepo
            accounts=AccountRepo(request=request).list(profile_id=selected_profile.id)
            context['accounts']=accounts
        if True:
                from projectmanager.views import EmployeeRepo,EmployeeSerializer
                employees=EmployeeRepo(request=request).list(profile_id=selected_profile.id)
                context['employees']=employees
                context['employees_s']=json.dumps(EmployeeSerializer(employees,many=True).data)



        return render(request,TEMPLATE_ROOT+"profile.html",context)
class ProfilesViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profiles=ProfileRepo(request=request).list(*args, **kwargs)
        context['profiles']=profiles
        print(profiles)
        return render(request,TEMPLATE_ROOT+"profiles.html",context)
class LoginViews(View):
    def get(self,request,*args, **kwargs):
        ProfileRepo(request=request).logout(request)
        pass
    def post(self,request):
        pass


class RegisterViews(View):
    def get(self,request,*args, **kwargs):
        ProfileRepo(request=request).logout(request)
        pass
    def post(self,request):
        pass


class LogoutViews(View):
    def get(self,request,*args, **kwargs):
        ProfileRepo(request=request).logout(request)
        return LoginViews().get(request=request)