
from core.constants import FAILED,SUCCEED
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.enums import ColorEnum
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View
from map.repo import AreaRepo, LocationRepo
from map.serializers import AreaSerializer, LocationSerializer
from accounting.views import add_from_accounts_context
from transport.forms import *
from utility.calendar import PersianCalendar 

from .serializers import ClientSerializer, DriverSerializer, MaintenanceSerializer,PassengerSerializer, ServiceManSerializer, TripCategorySerializer, TripPathSerializer, TripSerializer, VehicleSerializer, WorkShiftSerializer

from .repo import ClientRepo, MaintenanceRepo, ServiceManRepo,TripCategoryRepo, DriverRepo,PassengerRepo, TripPathRepo, TripRepo, VehicleRepo, WorkShiftRepo
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

    if not request.user.has_perm(APP_NAME+".add_trip"):
        return context
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

def get_work_shifts_context(request,*args, **kwargs):
    context={}
      
     #areas
    areas=AreaRepo(request=request).list(*args, **kwargs)
    context['areas']=areas
    areas_s=json.dumps(AreaSerializer(areas,many=True).data)
    context['areas_s']=areas_s
 

      
     #drivers
    drivers=DriverRepo(request=request).list(*args, **kwargs)
    context['drivers']=drivers
    drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
    context['drivers_s']=drivers_s
 
    #work_shifts
    work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
    context['work_shifts']=work_shifts
    work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
    context['work_shifts_s']=work_shifts_s



    if request.user.has_perm(APP_NAME+".add_workshift"):
        context['add_work_shif_form']=AddWorkShiftForm()

    return context

def get_add_maintenance_context(request,*args, **kwargs):
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

def get_add_work_event_context(request,*args, **kwargs):
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

        if request.user.has_perm(APP_NAME+".add_trippath"):
            context['add_trip_path_form']=AddTripPathForm()

            locations=LocationRepo(request=request).list()
            context['locations']=locations
            locations_s=json.dumps(LocationSerializer(locations,many=True).data)
            context['locations_s']=locations_s

            
            areas=AreaRepo(request=request).list()
            context['areas']=areas
            areas_s=json.dumps(AreaSerializer(areas,many=True).data)
            context['areas_s']=areas_s

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


class WorkShiftsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s
        return render(request,TEMPLATE_ROOT+"work-shifts.html",context)


class WorkShiftView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        work_shift=WorkShiftRepo(request=request).work_shift(*args, **kwargs)
        context['work_shift']=work_shift
        work_shift_s=json.dumps(WorkShiftSerializer(work_shift).data)
        context['work_shift_s']=work_shift_s
        context.update(get_transaction_context(request=request,transaction=work_shift))

        return render(request,TEMPLATE_ROOT+"work-shift.html",context)


class ServiceMansView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
        work_shifts_s=json.dumps(ServiceManSerializer(service_mans,many=True).data)
        context['work_shifts_s']=work_shifts_s
        return render(request,TEMPLATE_ROOT+"service-mans.html",context)


class ServiceManView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        service_man=ServiceManRepo(request=request).service_man(*args, **kwargs)
        context['service_man']=service_man
        service_man_s=json.dumps(ServiceManSerializer(service_man).data)
        context['service_man_s']=service_man_s
        context.update(get_account_context(request=request,account=service_man.account))


        #maintenances
        if False:
            trips=TripRepo(request=request).list(driver_id=driver.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s

        context.update(get_add_trip_context(request=request))

        

        return render(request,TEMPLATE_ROOT+"service-man.html",context)


class MaintenancesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances']=maintenances
        maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        context['maintenances_s']=maintenances_s
        return render(request,TEMPLATE_ROOT+"maintenances.html",context)


class MaintenanceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        maintenance=MaintenanceRepo(request=request).maintenance(*args, **kwargs)
        context['maintenance']=maintenance
        maintenance_s=json.dumps(MaintenanceSerializer(maintenance).data)
        context['maintenance_s']=maintenance_s
        context.update(get_transaction_context(request=request,transaction=maintenance))


        #maintenances
        if False:
            trips=TripRepo(request=request).list(driver_id=driver.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s

        # context.update(get_add_trip_context(request=request))

        

        return render(request,TEMPLATE_ROOT+"maintenance.html",context)


class DriverView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        driver=DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver
        context['driver_s']=json.dumps(DriverSerializer(driver).data)
        context.update(get_account_context(request=request,account=driver.account))


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
        if request.user.has_perm(APP_NAME+".add_driver"):
            context['add_driver_form']=AddDriverForm()
            context.update(add_from_accounts_context(request=request))
        return render(request,TEMPLATE_ROOT+"drivers.html",context)


class TripCategoriesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_categories=TripCategoryRepo(request=request).list(*args, **kwargs)
        context['trip_categories']=trip_categories
        trip_categories_s=json.dumps(TripCategorySerializer(trip_categories,many=True).data)
        context['trip_categories_s']=trip_categories_s
        if request.user.has_perm(APP_NAME+".add_tripcategory"):
            context['add_trip_category_form']=AddTripCategoryForm()
            context['colors']=(color[0] for color in ColorEnum.choices)
        return render(request,TEMPLATE_ROOT+"trip-categories.html",context)


class TripCategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_category=TripCategoryRepo(request=request).trip_category(*args, **kwargs)
        context['trip_category']=trip_category
        context['trip_category_s']=json.dumps(TripCategorySerializer(trip_category).data)
        #trips
        if True:
            trips=TripRepo(request=request).list(trip_category_id=trip_category.id)
            context['trips']=trips
            trips_s=json.dumps(TripSerializer(trips,many=True).data)
            context['trips_s']=trips_s


        if request.user.has_perm(APP_NAME+".add_trip"):
            context.update(get_add_trip_context(request=request))
            
        return render(request,TEMPLATE_ROOT+"trip-category.html",context)


class VehiclesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicles=VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s
        if request.user.has_perm(APP_NAME+".add_vehicle"):
            context['add_vehicle_form']=AddVehicleForm()
        return render(request,TEMPLATE_ROOT+"vehicles.html",context)


class VehicleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicle=VehicleRepo(request=request).vehicle(*args, **kwargs)
        context['vehicle']=vehicle
        vehicle_s=json.dumps(VehicleSerializer(vehicle).data)
        context['vehicle_s']=vehicle_s
        
        trips=TripRepo(request=request).list(vehicle_id=vehicle.id)
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips']=trips
        context['trips_s']=trips_s
        
        context.update(get_add_trip_context(request=request))
        context.update(get_work_shifts_context(request=request,vehicle_id=vehicle.id))
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
            cd['date_started']=PersianCalendar().to_gregorian(cd['date_started'])
            cd['date_ended']=PersianCalendar().to_gregorian(cd['date_ended'])
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
        context.update(get_account_context(request=request,account=passenger.account))
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
        if request.user.has_perm(APP_NAME+".add_passenger"):
            context['add_passenger_form']=AddPassengerForm()
            context.update(add_from_accounts_context(request=request))
        return render(request,TEMPLATE_ROOT+"passengers.html",context)


class ClientView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        client=ClientRepo(request=request).client(*args, **kwargs)
        context['client']=client
        context['client_s']=json.dumps(ClientSerializer(client).data)
        context.update(get_account_context(request=request,account=client.account))
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
        if request.user.has_perm(APP_NAME+".add_client"):
            context['add_client_form']=AddClientForm()
            context.update(add_from_accounts_context(request=request))
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
