from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from transport.forms import *
from transport.repo import ClientRepo, DriverRepo, MaintenanceRepo, PassengerRepo, TripCategoryRepo, TripPathRepo, VehicleRepo, WorkShiftRepo
from transport.serializers import ClientSerializer, DriverSerializer, PassengerSerializer, TripCategorySerializer, TripPathSerializer, VehicleSerializer, WorkShiftSerializer
from django.http import JsonResponse
 
class AddTripPathApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddTripPathForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            trip_path=TripPathRepo(request=request).add_trip_path(**cd)
            if trip_path is not None:
                context={
                    'result':SUCCEED,
                    'trip_path':TripPathSerializer(trip_path).data
                }
        return JsonResponse(context)

class AddClientApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        fm=AddClientForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            client=ClientRepo(request=request).add_client(**cd)
            if client is not None:
                context={
                    'result':SUCCEED,
                    'client':ClientSerializer(client).data
                }
        return JsonResponse(context)

    

   
class AddTripCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        fm=AddTripCategoryForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            trip_category=TripCategoryRepo(request=request).add_trip_category(**cd)
            if trip_category is not None:
                context={
                    'result':SUCCEED,
                    'trip_category':TripCategorySerializer(trip_category).data
                }
        return JsonResponse(context)

    

class AddDriverApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddDriverForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            driver=DriverRepo(request=request).add_driver(**cd)
            if driver is not None:
                context={
                    'result':SUCCEED,
                    'driver':DriverSerializer(driver).data
                }
        return JsonResponse(context)

    

class AddVehicleApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddVehicleForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            vehicle,message=VehicleRepo(request=request).add_vehicle(**cd)
            if vehicle is not None:
                context={
                    'result':SUCCEED,
                    'vehicle':VehicleSerializer(vehicle).data
                }
            else:
                context={
                    'result':FAILED,
                    'message':message
                }
        return JsonResponse(context)

    
class AddPassengerApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddPassengerForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            passenger=PassengerRepo(request=request).add_passenger(**cd)
            if passenger is not None:
                context={
                    'result':SUCCEED,
                    'passenger':PassengerSerializer(passenger).data
                }
        return JsonResponse(context)

    
    
class AddMaintenanceApi(APIView):
    def post(self,request,*args, **kwargs):
        
        context={
            'result':FAILED
        }
        fm=AddMaintenanceForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            work_shift=MaintenanceRepo(request=request).add_maintenance(**cd)
            if work_shift is not None:
                context={
                    'result':SUCCEED,
                    'work_shift':WorkShiftSerializer(work_shift).data
                }
        return JsonResponse(context)

    
class AddWorkShiftApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        fm=AddWorkShiftForm(request.POST)
        if fm.is_valid():
            cd=fm.cleaned_data
            work_shift=WorkShiftRepo(request=request).add_work_shift(**cd)
            if work_shift is not None:
                context={
                    'result':SUCCEED,
                    'work_shift':WorkShiftSerializer(work_shift).data
                }
        return JsonResponse(context)


