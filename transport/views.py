from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View

from .serializers import DriverSerializer,PassengerSerializer

from .repo import DriverRepo,PassengerRepo
from .apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json


TEMPLATE_ROOT = "transport/"
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
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s
        return render(request,TEMPLATE_ROOT+"index.html",context)

class DriverView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        driver=DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver
        return render(request,TEMPLATE_ROOT+"driver.html",context)

class TripPathView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        driver=DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver
        return render(request,TEMPLATE_ROOT+"trip-path.html",context)
class DriversView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s
        return render(request,TEMPLATE_ROOT+"drivers.html",context)

        
class PassengerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        passenger=PassengerRepo(request=request).passenger(*args, **kwargs)
        context['passenger']=passenger
        return render(request,TEMPLATE_ROOT+"passenger.html",context)

class PassengersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        passengers=PassengerRepo(request=request).list(*args, **kwargs)
        context['passengers']=passengers
        passengers_s=json.dumps(PassengerSerializer(passengers,many=True).data)
        context['passengers_s']=passengers_s
        return render(request,TEMPLATE_ROOT+"passengers.html",context)
class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
