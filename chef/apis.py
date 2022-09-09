from .serializers import FoodSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import FoodRepo
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

