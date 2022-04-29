from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render,reverse
from django.utils import timezone
from utility.apps import APP_NAME
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View

import json
from phoenix.server_settings import phoenix_apps
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "utility/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class ChartsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        return render(request,TEMPLATE_ROOT+"charts.html",context)

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        return render(request,TEMPLATE_ROOT+"index.html",context)
