from .serializers import FoodSerializer, ReservedMealSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import FoodRepo, ReservedMealRepo
from core.constants import SUCCEED, FAILED

class AddFoodApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            AddFoodForm_ = AddFoodForm(request.POST)
            if AddFoodForm_.is_valid():
                log += 1
                cd=AddFoodForm_.cleaned_data 
                
                food = FoodRepo(request=request).add_food(**cd)
                if food is not None:
                    context['food'] = FoodSerializer(food).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)


class ReserveMealApi(APIView):
    def post(self, request, *args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            reserve_meal_form=ReserveMealForm(request.POST)
            if reserve_meal_form.is_valid():
                log+=1
                reserved_meal=ReservedMealRepo(request=request).reserve_meal(**reserve_meal_form.cleaned_data)
                if reserved_meal is not None:
                    context['reserved_meal']=ReservedMealSerializer(reserved_meal).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)