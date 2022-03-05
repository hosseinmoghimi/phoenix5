from core.models import Page
from core.serializers import ParameterSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import PageRepo,  ParameterRepo
from .constants import SUCCEED, FAILED
from utility.utils import str_to_html

class ChangeParameterApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            change_parameter_form = ChangeParameterForm(request.POST)
            if change_parameter_form.is_valid():
                log += 1
                cd=change_parameter_form.cleaned_data
                parameter_id = cd['parameter_id']
                app_name = cd['app_name']
                parameter_name = cd['parameter_name']
                parameter_value = cd['parameter_value']
                
                parameter = ParameterRepo(request=request,app_name=app_name).change_parameter(
                    parameter_id=parameter_id,
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                    )
                if parameter is not None:
                    context['parameter'] = ParameterSerializer(parameter).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    