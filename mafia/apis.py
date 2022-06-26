from rest_framework.views import APIView

from core.constants import FAILED, SUCCEED
from mafia.serializers import *
from mafia.forms import *
from mafia.repo import GameRepo, RolePlayerRepo, RoleRepo
import json
from django.http import JsonResponse

class AddRoleToGameApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            frm=AddRoleToGameForm(request.POST)
            if frm.is_valid():
                log=3
                role_player=GameRepo(request=request).add_role_to_game(**frm.cleaned_data)
                
                if role_player is not None:
                    log=4
                    context['result']=SUCCEED
                    context['role_player']=RolePlayerSerializer(role_player).data
        context['log']=log
        return JsonResponse(context)
    
 
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
    
 
class AddPlayerToGameApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            frm=AddPlayerToGameForm(request.POST)
            if frm.is_valid():
                log=3
                cleaned_data=frm.cleaned_data
                # title=cleaned_data['title']
                # description=cleaned_data['description']
                role_player=RolePlayerRepo(request=request).add_role_player(**cleaned_data)
                if role_player is not None:
                    log=4
                    context['result']=SUCCEED
                    context['role_player']=RolePlayerSerializer(role_player).data
        context['log']=log
        return JsonResponse(context)
    
 