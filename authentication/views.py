from django.http import JsonResponse
from django.shortcuts import redirect, render,reverse
import json
from authentication.serializers import ProfileSerializer
from core.constants import FAILED, SUCCEED
from core.enums import ParameterNameEnum
from core.utils import app_is_installed
from .forms import *
from core.repo import PageLikeRepo, ParameterRepo
from .repo import ProfileRepo
from core.views import CoreContext, MessageView
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
        profiles=ProfileRepo(request=request).list(*args, **kwargs)
        context['profiles']=profiles
        context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class SearchViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profiles=ProfileRepo(request=request).list(*args, **kwargs)
        context['profiles']=profiles
        context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
        return render(request,TEMPLATE_ROOT+"search.html",context)
  
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            cd=search_form.cleaned_data
            search_for=cd['search_for']
            profiles=ProfileRepo(request=request).list(search_for=search_for)
            context['profiles']=ProfileSerializer(profiles).data
            context['result']=SUCCEED

        return JsonResponse(context)
class ProfileViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        selected_profile=ProfileRepo(request=request,forced=True).me
        if 'pk' in kwargs:
            selected_profile=ProfileRepo(request=request,forced=True).profile(*args, **kwargs)
        if selected_profile is None:
            mv=MessageView(request=request)
            mv.has_home_link=True
            mv.title="چنین پروفایلی پیدا نشد"
            return mv.show()

        context['selected_profile']=selected_profile
        
        if selected_profile.enabled:
            from accounting.views import AccountRepo
            accounts=AccountRepo(request=request).list(profile_id=selected_profile.id)
            context['accounts']=accounts
        if selected_profile.enabled:
            if app_is_installed('projectmanager'):
                from projectmanager.views import EmployeeRepo,EmployeeSerializer
                employees=EmployeeRepo(request=request).list(profile_id=selected_profile.id)
                context['employees']=employees
                context['employees_s']=json.dumps(EmployeeSerializer(employees,many=True).data)

                
        if not selected_profile.enabled:
            context['no_navbar']=True
            context['no_footer']=True


        page_likes=PageLikeRepo(request=request).list(profile_id=selected_profile.id)
        context['page_likes']=page_likes



        profiles=ProfileRepo(request=request).list(user_id=selected_profile.user.id)
        if len(profiles)>1:
            context['profiles']=profiles
            context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
            context['set_default_profile_form']=SetDefaultProfileForm()

        return render(request,TEMPLATE_ROOT+"profile.html",context)



class ChangeProfileImageViews(View):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        profile_id=0
        if 'pk' in kwargs:
            profile_id=kwargs['pk']
        log=1
        if request.method=='POST':
            log=2
            edit_profile_form=ChangeProfileImageForm(request.POST,request.FILES)
            if edit_profile_form.is_valid():
                log=3              
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                image=request.FILES['image']
                result=ProfileRepo(request=request).change_profile_image(profile_id=profile_id,
                image=image,
                )
        return redirect(reverse(APP_NAME+":profile",kwargs={'pk':profile_id}))


class EditProfileViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        selected_profile=ProfileRepo(request=request,forced=True).me
        if 'pk' in kwargs:
            selected_profile=ProfileRepo(request=request,forced=True).profile(*args, **kwargs)
        if selected_profile is None:
            mv=MessageView(request=request)
            mv.has_home_link=True
            mv.title="چنین پروفایلی پیدا نشد"
            return mv.show()
        context['edit_profile_form']=EditProfileForm()
        context['selected_profile']=selected_profile
        context['selected_profile_s']=json.dumps(ProfileSerializer(selected_profile).data)
     
        return render(request,TEMPLATE_ROOT+"edit-profile.html",context)

    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        profile_id=0
        if 'pk' in kwargs:
            profile_id=kwargs['pk']
        log=1
        if request.method=='POST':
            log=2
            edit_profile_form=EditProfileForm(request.POST)
            if edit_profile_form.is_valid():
                log=3              
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                first_name=edit_profile_form.cleaned_data['first_name']
                last_name=edit_profile_form.cleaned_data['last_name']
                email=edit_profile_form.cleaned_data['email']
                bio=edit_profile_form.cleaned_data['bio']
                mobile=edit_profile_form.cleaned_data['mobile']
                address=edit_profile_form.cleaned_data['address']
                result=ProfileRepo(request=request).edit_profile(profile_id=profile_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                bio=bio,
                mobile=mobile,
                address=address,
                )
                if result:
                    context['result']=SUCCEED

        context['log']=log
        return JsonResponse(context)  


class ProfilesViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        profiles=ProfileRepo(request=request).list(*args, **kwargs)
        context['profiles']=profiles
        context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
        return render(request,TEMPLATE_ROOT+"profiles.html",context)


class LoginViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        ProfileRepo(request=request).logout(request)
        context['login_form']=LoginForm()
        context['build_absolute_uri']=request.build_absolute_uri()
        build_absolute_uri=request.build_absolute_uri()
        print(build_absolute_uri)
        ONLY_HTTPS=ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterNameEnum.ONLY_HTTPS,default=False).boolean_value
        if ONLY_HTTPS and "http://" in build_absolute_uri :
            build_absolute_uri="https://"+build_absolute_uri[7:]
            return redirect(build_absolute_uri)
        return render(request,TEMPLATE_ROOT+"login.html",context)  
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            a=ProfileRepo(request=request).login(request=request,username=username,password=password)
            if a is not None:
                (request,user)=a
                return redirect(APP_NAME+":me")


class LoginAsViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if request.user.has_perm(APP_NAME+".change_profile"):
            selected_profile=ProfileRepo(request=request).profile(*args, **kwargs)
            if selected_profile is not None:
                ProfileRepo(request=request).login(request=request,user=selected_profile.user)
                return redirect(APP_NAME+":me")
        return redirect(APP_NAME+":login")


class RegisterViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['register_form']=RegisterForm()
        return render(request,TEMPLATE_ROOT+"register.html",context)  
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            a=register_form.save()
            a=ProfileRepo(request=request).login(request=request,user=a)
            return redirect(APP_NAME+":me")


class LogoutViews(View):
    def get(self,request,*args, **kwargs):
        ProfileRepo(request=request).logout(request)
        return LoginViews().get(request=request)