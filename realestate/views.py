from django.shortcuts import render,reverse
from accounting.repo import AccountRepo
from authentication.repo import ProfileRepo
from core.views import CoreContext, MessageView, PageContext,ParameterNameEnum,ParameterRepo
from realestate.enums import *
from realestate.repo import PropertyRepo
from realestate.serializers import  PropertySerializer
from realestate.apps import APP_NAME
from django.views import View
from realestate.forms import *
import json

from accounting.views import add_from_accounts_context


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
        # return PropertiesView().get(request=request,*args, **kwargs)
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class PropertiesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        properties=PropertyRepo(request=request).list(*args, **kwargs)
        context['properties']=properties
        context['properties_s']=json.dumps(PropertySerializer(properties,many=True).data)
        if self.request.user.has_perm(APP_NAME+".add_property"):
            context['add_property_form']=AddPropertyForm()
            context.update(add_from_accounts_context(request=request))
        return render(request,TEMPLATE_ROOT+"properties.html",context)


class PropertyView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        property=PropertyRepo(request=request).property(*args, **kwargs)
        context.update(PageContext(request=request,page=property))
        context['property']=property
        context['property_s']=json.dumps(PropertySerializer(property).data)


        return render(request,TEMPLATE_ROOT+"property.html",context)



class AgentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        agent=AccountRepo(request=request).account(*args, **kwargs)
        context['agent']=agent

        properties=PropertyRepo(request=request).list(agent_id=agent.id)
        context['properties']=properties
        context['properties_s']=json.dumps(PropertySerializer(properties,many=True).data)

        return render(request,TEMPLATE_ROOT+"agent.html",context)



class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
 
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)


        return render(request,TEMPLATE_ROOT+"index.html",context)

