from .serializers import DrugSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import DrugRepo
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
