from django.shortcuts import render,reverse
from authentication.repo import ProfileRepo
from core.views import CoreContext, MessageView, PageContext,ParameterNameEnum,ParameterRepo
from health.repo import DrugRepo, PatientRepo
from health.serializers import DrugSerializer, PatientSerializer
from health.enums import *
from health.apps import APP_NAME
from django.views import View
from health.forms import *
import json

TEMPLATE_ROOT="health/"
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


class PatientsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        patients=PatientRepo(request=request).list(*args, **kwargs)
        context['patients']=patients
        context['patients_s']=json.dumps(PatientSerializer(patients,many=True).data)
        return render(request,TEMPLATE_ROOT+"patients.html",context)


class PatientView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        patient=PatientRepo(request=request).patient(*args, **kwargs)
        context['patient']=patient
        return render(request,TEMPLATE_ROOT+"patient.html",context)




class DrugsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drugs=DrugRepo(request=request).list(*args, **kwargs)
        context['drugs']=drugs
        context['drugs_s']=json.dumps(DrugSerializer(drugs,many=True).data)
        
        if request.user.has_perm(APP_NAME+".add_drug"):
            context['add_drug_form']=AddDrugForm()

        return render(request,TEMPLATE_ROOT+"drugs.html",context)


class DrugView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drug=DrugRepo(request=request).drug(*args, **kwargs)
        context['drug']=drug
        return render(request,TEMPLATE_ROOT+"drug.html",context)



class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)

