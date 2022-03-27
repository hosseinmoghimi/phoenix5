from django.http import Http404, JsonResponse
from django.shortcuts import render,reverse
from core.constants import CURRENCY, FAILED, SUCCEED 
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View

from utility.calendar import PersianCalendar
from .apps import APP_NAME
# 
import json


LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "wallet/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    # context['search_form'] = SearchForm()
    # context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context
 


class SearchView(View):
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context['search_for']=search_for
            folders=FolderRepo(request=request).list(search_for=search_for)
            context['folders']=folders
        return render(request,TEMPLATE_ROOT+"folder.html",context)




class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context) 