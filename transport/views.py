
from core.constants import FAILED,SUCCEED
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View

from transport.forms import * 

from .serializers import ClientSerializer, DriverSerializer,PassengerSerializer, TripPathSerializer, TripSerializer, VehicleSerializer

from .repo import ClientRepo,TripCategoryRepo, DriverRepo,PassengerRepo, TripPathRepo, TripRepo, VehicleRepo
from .apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
from accounting.views import get_transaction_context,get_account_context

TEMPLATE_ROOT = "transport/"
LAYOUT_PARENT = "phoenix/layout.html"

def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context

def get_add_trip_context(request,*args, **kwargs):
    context={}

     #vehicles
    vehicles=VehicleRepo(request=request).list(*args, **kwargs)
    context['vehicles']=vehicles
    vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
    context['vehicles_s']=vehicles_s

     #trip_categories
    trip_categories=TripCategoryRepo(request=request).list(*args, **kwargs)
    context['trip_categories']=trip_categories 



     #clients
    clients=ClientRepo(request=request).list(*args, **kwargs)
    context['clients']=clients
    clients_s=json.dumps(ClientSerializer(clients,many=True).data)
    context['clients_s']=clients_s



     #drivers
    drivers=DriverRepo(request=request).list(*args, **kwargs)
    context['drivers']=drivers
    drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
    context['drivers_s']=drivers_s


    #passengers
    passengers=PassengerRepo(request=request).list(*args, **kwargs)
    context['passengers']=passengers
    passengers_s=json.dumps(PassengerSerializer(passengers,many=True).data)
    context['passengers_s']=passengers_s
    

    #trip_paths
    trip_paths=TripPathRepo(request=request).list(*args, **kwargs)
    context['trip_paths']=trip_paths
    trip_paths_s=json.dumps(TripPathSerializer(trip_paths,many=True).data)
    context['trip_paths_s']=trip_paths_s

    context['add_trip_form']=AddTripForm()
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s
        return render(request,TEMPLATE_ROOT+"index.html",context)


class TripPathsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_paths=TripPathRepo(request=request).list(*args, **kwargs)
        context['trip_paths']=trip_paths
        trip_paths_s=json.dumps(TripPathSerializer(trip_paths,many=True).data)
        context['trip_paths_s']=trip_paths_s
        return render(request,TEMPLATE_ROOT+"trip-paths.html",context)


class TripPathView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_path=TripPathRepo(request=request).trip_path(*args, **kwargs)
        context['trip_path']=trip_path
        context['trip_path_s']=json.dumps(TripPathSerializer(trip_path).data)


        trips=trip_path.trip_set.all()
        context['trips']=trips
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips_s']=trips_s


        context.update(get_add_trip_context(request=request))
        return render(request,TEMPLATE_ROOT+"trip-path.html",context)


class TripsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips_s']=trips_s
        return render(request,TEMPLATE_ROOT+"trips.html",context)


class TripView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip=TripRepo(request=request).trip(*args, **kwargs)
        context['trip']=trip
        passengers=trip.passengers.all()
        context['passengers']=passengers
        passengers_s=json.dumps(PassengerSerializer(passengers,many=True).data)
        context['passengers_s']=passengers_s
        context.update(get_transaction_context(request=request,transaction=trip))
        return render(request,TEMPLATE_ROOT+"trip.html",context)


class DriverView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        driver=DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver
        context['driver_s']=json.dumps(DriverSerializer(driver).data)
        context.update(get_account_context(request=request,account=driver))


        #trips
        if True:
            trips=TripRepo(request=request).list(driver_id=driver.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s

        context.update(get_add_trip_context(request=request))

        return render(request,TEMPLATE_ROOT+"driver.html",context)


class DriversView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s
        return render(request,TEMPLATE_ROOT+"drivers.html",context)

   
class VehiclesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicles=VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s
        return render(request,TEMPLATE_ROOT+"vehicles.html",context)


class VehicleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicle=VehicleRepo(request=request).vehicle(*args, **kwargs)
        context['vehicle']=vehicle
        vehicle_s=json.dumps(VehicleSerializer(vehicle).data)
        context['vehicle_s']=vehicle_s

        context.update(get_add_trip_context(request=request))
        return render(request,TEMPLATE_ROOT+"vehicle.html",context)

   
class AddTripPathView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s
        return render(request,TEMPLATE_ROOT+"add-trip-path.html",context)
        

class AddTripView(View):

    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_add_trip_context(request=request))
        context['show_add_trip_form_collapse']=True
        return render(request,TEMPLATE_ROOT+"add-trip.html",context)

    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        fm=AddTripForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            cd['passengers']=json.loads(cd['passengers'])
            cd['trip_paths']=json.loads(cd['trip_paths'])
            trip=TripRepo(request=request).add_trip(**cd)
            if trip is not None:
                context['trip']=TripSerializer(trip).data
                context['result']=SUCCEED
        return JsonResponse(context)
            
class PassengerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        passenger=PassengerRepo(request=request).passenger(*args, **kwargs)
        context['passenger']=passenger
        context['passenger_s']=json.dumps(PassengerSerializer(passenger).data)
        context.update(get_account_context(request=request,account=passenger))
        context.update(get_add_trip_context(request=request))

        #trips
        if True:
            trips=TripRepo(request=request).list(passenger_id=passenger.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s
        return render(request,TEMPLATE_ROOT+"passenger.html",context)


class PassengersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        passengers=PassengerRepo(request=request).list(*args, **kwargs)
        context['passengers']=passengers
        passengers_s=json.dumps(PassengerSerializer(passengers,many=True).data)
        context['passengers_s']=passengers_s
        return render(request,TEMPLATE_ROOT+"passengers.html",context)


class ClientView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        client=ClientRepo(request=request).client(*args, **kwargs)
        context['client']=client
        context['client_s']=json.dumps(ClientSerializer(client).data)
        context.update(get_account_context(request=request,account=client))
        context.update(get_add_trip_context(request=request))

        #trips
        if True:
            trips=TripRepo(request=request).list(client_id=client.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s
        return render(request,TEMPLATE_ROOT+"client.html",context)


class ClientsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        clients=ClientRepo(request=request).list(*args, **kwargs)
        context['clients']=clients
        clients_s=json.dumps(ClientSerializer(clients,many=True).data)
        context['clients_s']=clients_s
        return render(request,TEMPLATE_ROOT+"clients.html",context)


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
