from django.shortcuts import redirect, render
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

    # parameter_repo = ParameterRepo(request=request,app_name=APP_NAME)
    return context
# Create your views here.
class BasicViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profiles=ProfileRepo(request=request).list()
        context['profiles']=profiles
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProfileViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profile=ProfileRepo(request=request).me
        context['selected_profile']=profile
        return render(request,TEMPLATE_ROOT+"profile.html",context)
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