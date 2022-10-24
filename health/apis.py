from .serializers import DrugSerializer, PatientSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import DrugRepo, PatientRepo
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
