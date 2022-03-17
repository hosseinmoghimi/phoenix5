from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm,PageContext
# Create your views here.
from django.views import View
from .apps import APP_NAME
# from .repo import MaterialRepo
# from .serializers import MaterialSerializer
import json
from .repo import MaterialRepo,ServiceRepo
from .serializers import MaterialSerializer,ServiceSerializer

TEMPLATE_ROOT = "projectmanager/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"index.html",context)



class MaterialsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        materials=MaterialRepo(request=request).list()
        context['materials']=materials
        materials_s=json.dumps(MaterialSerializer(materials,many=True).data)
        context['materials_s']=materials_s
        return render(request,TEMPLATE_ROOT+"materials.html",context)

class MaterialView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        material=MaterialRepo(request=request).material(*args, **kwargs)
        context.update(PageContext(request=request,page=material))
        context['material']=material
        return render(request,TEMPLATE_ROOT+"material.html",context)

class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        return render(request,TEMPLATE_ROOT+"services.html",context)

class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service=ServiceRepo(request=request).service(*args, **kwargs)
        context.update(PageContext(request=request,page=service))
        context['service']=service
        return render(request,TEMPLATE_ROOT+"service.html",context)
        