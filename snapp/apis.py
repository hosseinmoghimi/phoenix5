from .apps import APP_NAME
from core.apis import APIView,JsonResponse
from .forms import *



class UpdatePrices(APIView):
    def post(self,request,*args, **kwargs):
        update_price_form=UpdatePricesForm(request.POST)
        if update_price_form.is_valid():
            pass