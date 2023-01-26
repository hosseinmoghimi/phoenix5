from django.shortcuts import render,reverse
from authentication.repo import ProfileRepo
from core.views import CoreContext, MessageView, PageContext,ParameterNameEnum,ParameterRepo
from health.repo import DiseaseRepo, DoctorRepo, DrugRepo, PatientRepo
from health.serializers import DiseaseSerializer, DoctorSerializer, DrugSerializer, PatientSerializer, VisitSerializer
from health.enums import *
from health.apps import APP_NAME
from django.views import View
from accounting.views import add_from_accounts_context
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
        if request.user.has_perm(APP_NAME+".add_patient"):
            context.update(add_from_accounts_context(request=request))
            context['add_patient_form']=AddPatientForm()
        context['patients_s']=json.dumps(PatientSerializer(patients,many=True).data)
        return render(request,TEMPLATE_ROOT+"patients.html",context)


class PatientView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        patient=PatientRepo(request=request).patient(*args, **kwargs)
        context['patient']=patient
        visits=patient.visit_set.all()
        context['visits']=visits
        visits_s=json.dumps(VisitSerializer(visits,many=True).data)
        context['visits_s']=visits_s
        return render(request,TEMPLATE_ROOT+"patient.html",context)


class DoctorsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        doctors=DoctorRepo(request=request).list(*args, **kwargs)
        context['doctors']=doctors
        if request.user.has_perm(APP_NAME+".add_doctor"):
            context.update(add_from_accounts_context(request=request))
            context['add_doctor_form']=AddDoctorForm()
        context['doctors_s']=json.dumps(DoctorSerializer(doctors,many=True).data)
        return render(request,TEMPLATE_ROOT+"doctors.html",context)


class DoctorView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        doctor=DoctorRepo(request=request).doctor(*args, **kwargs)
        context['doctor']=doctor
        return render(request,TEMPLATE_ROOT+"doctor.html",context)



class VisitsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        doctors=DoctorRepo(request=request).list(*args, **kwargs)
        context['doctors']=doctors
        if request.user.has_perm(APP_NAME+".add_doctor"):
            context.update(add_from_accounts_context(request=request))
            context['add_doctor_form']=AddDoctorForm()
        context['doctors_s']=json.dumps(DoctorSerializer(doctors,many=True).data)
        return render(request,TEMPLATE_ROOT+"visits.html",context)


class VisitView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        doctor=DoctorRepo(request=request).doctor(*args, **kwargs)
        context['doctor']=doctor
        return render(request,TEMPLATE_ROOT+"visit.html",context)



class DiseasesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        diseases=DiseaseRepo(request=request).list(*args, **kwargs)
        context['diseases']=diseases
        context['diseases_s']=json.dumps(DiseaseSerializer(diseases,many=True).data)
        if request.user.has_perm(APP_NAME+".add_disease"):
            context['add_disease_form']=AddDiseaseForm()
        return render(request,TEMPLATE_ROOT+"diseases.html",context)


class DiseaseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        disease=DiseaseRepo(request=request).disease(*args, **kwargs)
        # context.update(PageContext(request=request,page=disease))
        context['disease']=disease
        return render(request,TEMPLATE_ROOT+"disease.html",context)





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
        context.update(PageContext(request=request,page=drug))
        context['drug']=drug


        
        diseases=drug.disease_set.all()
        context['diseases']=diseases
        context['diseases_s']=json.dumps(DiseaseSerializer(diseases,many=True).data)
        
        return render(request,TEMPLATE_ROOT+"drug.html",context)



class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list(*args, **kwargs)
        context['books']=books
        context['books_s']=json.dumps(BookSerializer(books,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)

