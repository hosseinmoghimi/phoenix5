from realestate.forms import *
from realestate.repo import PropertyRepo
from realestate.serializers import PropertySerializer
from core.apis import FAILED,SUCCEED,JsonResponse,APIView
class AddPropertyApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        log=2
        add_property_form=AddPropertyForm(request.POST)
        if add_property_form.is_valid():
            log=3
            property=PropertyRepo(request=request).add_property(**add_property_form.cleaned_data)
            if property is not None:
                log=4
                context['result']=SUCCEED
                context['property']=PropertySerializer(property).data
        context['log']=log
        return JsonResponse(context)