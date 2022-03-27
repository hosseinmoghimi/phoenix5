from rest_framework.views import APIView
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer
from django.http import JsonResponse
from authentication.forms import *
from core.constants import FAILED, SUCCEED



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
