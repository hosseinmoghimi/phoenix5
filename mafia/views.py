import json
from django.shortcuts import render
from django.views import View
from core.apps import APP_NAME
from core.views import CoreContext,PageContext
from mafia.enums import RoleSideEnum
from mafia.forms import AddRoleForm
from mafia.repo import RoleRepo
from mafia.serializers import RoleSerializer

TEMPLATE_ROOT="mafia/"
LAYOUT_PARENT="phoenix/layout.html"
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['go']="go go go !"
        return render(request,TEMPLATE_ROOT+"index.html",context)


class RolesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        roles=RoleRepo(request=request).list(*args, **kwargs)
        context['roles']=roles
        roles_s=json.dumps(RoleSerializer(roles,many=True).data)
        context['roles_s']=roles_s
        if request.user.has_perm(APP_NAME+".add_role"):
            context['sides']=(side[0] for side in RoleSideEnum.choices)
            context['add_role_form']=AddRoleForm()
        return render(request,TEMPLATE_ROOT+"roles.html",context)

class RoleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        role=RoleRepo(request=request).role(*args, **kwargs)
        context['role']=role
        return render(request,TEMPLATE_ROOT+"role.html",context)


