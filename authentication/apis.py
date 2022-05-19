from rest_framework.views import APIView
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer
from django.http import JsonResponse
from authentication.forms import *
from core.constants import FAILED, SUCCEED

class LoginApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            (request,profile,token,created)=ProfileRepo(request=request).authenticate_for_apk(username=username,password=password)
            if profile is not None:
                context['profile']=ProfileSerializer(profile).data
                context['token']=token
                context['result']=SUCCEED
                context['created']=created
        return JsonResponse(context)

class AddProfileApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        message=None
        message=" sfh sdjfh sldjk skdlfh ksdjlhf lks"
        profile=None
        log=2
        result=FAILED
        add_profile_form=AddProfileForm(request.POST)
        if add_profile_form.is_valid():
            log=3
            cd=add_profile_form.cleaned_data
            (result,profile,message)=ProfileRepo(request=request).add_profile(**cd)
            if profile is not None:
                log=4
                profile=ProfileSerializer(profile).data
        context['profile']=profile
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)


class SetDefaultProfileApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        set_default_profile_form=SetDefaultProfileForm(request.POST)
        if set_default_profile_form.is_valid():
            profile_id=set_default_profile_form.cleaned_data['profile_id']
            profile=ProfileRepo(request=request).set_default(profile_id=profile_id)
            if profile is not None:
                context['result']=SUCCEED
        return JsonResponse(context)
