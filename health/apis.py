from .serializers import DiseaseSerializer, DrugSerializer, PatientSerializer,DoctorSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import DiseaseRepo, DrugRepo, PatientRepo,DoctorRepo
from core.constants import SUCCEED, FAILED

class AddDrugApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            AddDrugForm_ = AddDrugForm(request.POST)
            if AddDrugForm_.is_valid():
                log += 1
                cd=AddDrugForm_.cleaned_data 
                
                drug = DrugRepo(request=request).add_drug(**cd)
                if drug is not None:
                    context['drug'] = DrugSerializer(drug).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

class AddPatientApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            AddDrugForm_ = AddPatientForm(request.POST)
            if AddDrugForm_.is_valid():
                log += 1
                cd=AddDrugForm_.cleaned_data 
                
                patient,result,message = PatientRepo(request=request).add_patient(**cd)
                if result==SUCCEED and patient is not None:
                    context['patient'] = PatientSerializer(patient).data
                context['result'] = result
                context['message'] = message
        context['log'] = log
        return JsonResponse(context)

class AddDiseaseApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            AddDiseaseForm_ = AddDiseaseForm(request.POST)
            if AddDiseaseForm_.is_valid():
                log += 1
                cd=AddDiseaseForm_.cleaned_data 
                
                disease,result,message = DiseaseRepo(request=request).add_disease(**cd)
                if result==SUCCEED and disease is not None:
                    context['disease'] = DiseaseSerializer(disease).data
                context['result'] = result
                context['message'] = message
        context['log'] = log
        return JsonResponse(context)

class AddDoctorApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            AddDrugForm_ = AddDoctorForm(request.POST)
            if AddDrugForm_.is_valid():
                log += 1
                cd=AddDrugForm_.cleaned_data 
                
                doctor,result,message = DoctorRepo(request=request).add_doctor(**cd)
                if result==SUCCEED and doctor is not None:
                    context['doctor'] = DoctorSerializer(doctor).data
                context['result'] = result
                context['message'] = message
        context['log'] = log
        return JsonResponse(context)
