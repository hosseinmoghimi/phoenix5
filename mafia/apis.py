from rest_framework.views import APIView

from core.constants import FAILED, SUCCEED
from mafia.serializers import *
from mafia.forms import *
from mafia.repo import RoleRepo
import json
from django.http import JsonResponse


class AddRoleApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            frm=AddRoleForm(request.POST)
            if frm.is_valid():
                log=3
                cleaned_data=frm.cleaned_data
                # title=cleaned_data['title']
                # description=cleaned_data['description']
                role=RoleRepo(request=request).add_role(**cleaned_data)
                
                if role is not None:
                    log=4
                    context['result']=SUCCEED
                    context['role']=RoleSerializer(role).data
        context['log']=log
        return JsonResponse(context)
    
 