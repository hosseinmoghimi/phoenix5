from django.shortcuts import render
from chef.forms import *
from chef.repo import FoodRepo, GuestRepo, HostRepo, MealRepo
from chef.serializers import FoodSerializer, GuestSerializer, HostSerializer, MealSerializer
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
    me_guest=GuestRepo(request=request).me
    context['me_guest']=me_guest
    me_guest_s=json.dumps(GuestSerializer(me_guest).data)
    context['me_guest_s']=me_guest_s
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


class HostsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        hosts=HostRepo(request=request).list(*args, **kwargs)
        context['hosts']=hosts
        hosts_s=json.dumps(HostSerializer(hosts,many=True).data)
        context['hosts_s']=hosts_s
        
        if request.user.has_perm(APP_NAME+".add_host"):
            context['add_host_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"hosts.html",context)



class HostView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        host=HostRepo(request=request).host(*args, **kwargs)
        context['host']=host
        host_s=json.dumps(HostSerializer(host,many=False).data)
        context['host_s']=host_s
        
        if request.user.has_perm(APP_NAME+".add_host"):
            context['add_host_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"host.html",context)


class MealsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        meals=MealRepo(request=request).list(*args, **kwargs)
        context['meals']=meals
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context['meals_s']=meals_s
        guests=[]
        guests_s=json.dumps(GuestSerializer(guests,many=True).data)
        context['guests_s']=guests_s
        
        if request.user.has_perm(APP_NAME+".add_guest"):
            context['add_guest_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"meals.html",context)


class MealView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        meal=MealRepo(request=request).meal(*args, **kwargs)
        context['meal']=meal
        meal_s=json.dumps(MealSerializer(meal,many=False).data)
        context['meal_s']=meal_s
        
        if request.user.has_perm(APP_NAME+".add_guest"):
            context['add_guest_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"meal.html",context)

class GuestsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        guests=GuestRepo(request=request).list(*args, **kwargs)
        context['guests']=guests
        guests_s=json.dumps(GuestSerializer(guests,many=True).data)
        context['guests_s']=guests_s
        
        if request.user.has_perm(APP_NAME+".add_guest"):
            context['add_guest_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"guests.html",context)


class GuestView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        guest=GuestRepo(request=request).guest(*args, **kwargs)
        context['guest']=guest
        guest_s=json.dumps(GuestSerializer(guest,many=False).data)
        context['guest_s']=guest_s
        
        if request.user.has_perm(APP_NAME+".add_guest"):
            context['add_guest_form']=AddFoodForm()

        return render(request,TEMPLATE_ROOT+"guest.html",context)


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