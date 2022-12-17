from django.shortcuts import render
from .apps import APP_NAME
from django.http import Http404
from django.views import View
from core.views import CoreContext
from core.repo import ParameterRepo
LAYOUT_PARENT="phoenix/layout.html"

TEMPLATE_ROOT="loyaltyclub/"
def getContext(*args, **kwargs):
    if 'request' in kwargs:
        request=kwargs['request']

    if request is None:
        return Http404
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    # context['APP_NAME']=APP_NAME
    return context
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['card_title']=parameter_repo.parameter(name="عنوان کارت ایندکس",default="باشگاه مشتریان")

        return render(request,TEMPLATE_ROOT+"index.html",context)