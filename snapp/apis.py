from .apps import APP_NAME
from core.apis import APIView,JsonResponse,FAILED,SUCCEED
from .forms import *
from .repo import MenuRepo
from .serializers import MenuSerializer


class UpdatePrices(APIView):
    def post(self,request,*args, **kwargs):
        update_price_form=UpdatePricesForm(request.POST)
        if update_price_form.is_valid():
            pass

class AddMenuView(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message="داده های فرم نامعتبر"
        add_menu_form=AddMenuForm(request.POST)
        if add_menu_form.is_valid():
            result,menu,message=MenuRepo(request=request).add_menu(**add_menu_form.cleaned_data)
            context['menu']=MenuSerializer(menu).data
        context['result']=result
        context['message']=message
        return JsonResponse(context)
