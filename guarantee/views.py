from django.http import Http404, JsonResponse
from django.shortcuts import render,reverse
from core.constants import CURRENCY, FAILED, SUCCEED 
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View
from guarantee.enums import GuaranteeStatusEnum, GuaranteeTypeEnum
from guarantee.forms import *
from guarantee.repo import GuaranteeRepo

from utility.calendar import PersianCalendar
from guarantee.serializers import GuaranteeSerializer
from .apps import APP_NAME
# 
import json


LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = APP_NAME+"/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    # context['search_form'] = SearchForm()
    # context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


def get_add_guarantee_context(request,*args, **kwargs):
    
    context={}
    guarantee_types=(i[0] for i in GuaranteeTypeEnum.choices)
    guarantee_statuses=(i[0] for i in GuaranteeStatusEnum.choices)
    context['guarantee_statuses']=guarantee_statuses
    context['guarantee_types']=guarantee_types
    context['add_guarantee_form']=AddGuaranteeForm()
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        return GuaranteesViews().get(request=request,*args, **kwargs)

class GuaranteeViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        guarantee=GuaranteeRepo(request=request).guarantee(*args, **kwargs)
        context['guarantee']=guarantee
        return render(request,TEMPLATE_ROOT+"guarantee.html",context)
    
class GuaranteesViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        guarantees=GuaranteeRepo(request=request).list(*args, **kwargs)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s
        return render(request,TEMPLATE_ROOT+"guarantees.html",context)
    
