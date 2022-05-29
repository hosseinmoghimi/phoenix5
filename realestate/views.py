from django.shortcuts import render,reverse
from authentication.repo import ProfileRepo
from core.views import CoreContext, MessageView, PageContext,ParameterNameEnum,ParameterRepo
from realestate.enums import *
from realestate.repo import PropertyRepo
from realestate.serializers import  PropertySerializer
from realestate.apps import APP_NAME
from django.views import View
from realestate.forms import *
import json

TEMPLATE_ROOT="realestate/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['search_form']=SearchForm()
    
    context['search_action'] = reverse(APP_NAME+":search")
 
    return context

class HomeViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
       


        return render(request,TEMPLATE_ROOT+"index.html",context)


class PropertiesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        properties=PropertyRepo(request=request).list(*args, **kwargs)
        context['properties']=properties
        context['properties_s']=json.dumps(PropertySerializer(properties,many=True).data)


        return render(request,TEMPLATE_ROOT+"properties.html",context)


class PropertyView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)


        return render(request,TEMPLATE_ROOT+"index.html",context)



class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)


        return render(request,TEMPLATE_ROOT+"index.html",context)

