from django.shortcuts import render
from chef.forms import *
from chef.repo import FoodRepo
from chef.serializers import FoodSerializer
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext, PageContext
# Create your views here.
from django.views import View
from chef.apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json


TEMPLATE_ROOT = "chef/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchView(View):
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            cd=search_form.cleaned_data
            foods=FoodRepo(request=request).list(**cd)
            context['foods']=foods
            foods_s=json.dumps(FoodSerializer(foods,many=True).data)
            context['foods_s']=foods_s
        return render(request,TEMPLATE_ROOT+"foods.html",context)

class FoodsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        foods=FoodRepo(request=request).list()
        context['foods']=foods
        foods_s=json.dumps(FoodSerializer(foods,many=True).data)
        context['foods_s']=foods_s
        if request.user.has_perm(APP_NAME+".add_food"):
            context['add_food_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"foods.html",context)


class FoodView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        food=FoodRepo(request=request).food(*args, **kwargs)
        context.update(PageContext(request=request,page=food))
        context['food']=food
        return render(request,TEMPLATE_ROOT+"food.html",context)