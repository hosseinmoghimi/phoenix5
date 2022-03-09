from django.shortcuts import render
from django.views import View
from .apps import APP_NAME
from core.views import CoreContext
from authentication.repo import ProfileRepo

TEMPLATE_ROOT="stock/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
# Create your views here.
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)