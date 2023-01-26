from core.constants import FAILED, SUCCEED
from transport.apps import APP_NAME
from transport.serializers import MaintenanceSerializer
from .models import Driver, Luggage, Maintenance,Passenger,ServiceMan, Trip, TripCategory, TripPath, Vehicle,Client, WorkShift
from authentication.repo import ProfileRepo
from django.utils import timezone
from django.db.models import Q

class DriverRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Driver.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_driver(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_driver"):
            return
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            driver=self.driver(account_id=account_id)

            if driver is None:
                driver=Driver(account_id=account_id)
                if 'title' in kwargs:
                    driver.title=kwargs['title']
                driver.save()
                return driver
        

    def driver(self, *args, **kwargs):
        pk=0
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            return self.objects.filter(account_id=account_id).first()
        if 'driver_id' in kwargs:
            pk=kwargs['driver_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class LuggageRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Luggage.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_luggage(self,*args, **kwargs):
        result=FAILED
        message="خطا در افزودن بار"
        luggage=None
        if not self.user.has_perm(APP_NAME+".add_driver"):
            message="دسترسی غیر مجاز"
            return luggage,message,result
        luggage=Luggage(*args, **kwargs)
        # if 'owner_id' in kwargs:
        #     owner_id=kwargs['owner_id']
        #     luggage.owner_id=owner_id
        # if 'title' in kwargs:
        #     title=kwargs['title']
        #     luggage.title=title
        luggage.save() 
        result=SUCCEED
        message="بار با موفقیت اضافه شد."
        return luggage,message,result
        

    def luggage(self, *args, **kwargs):
        pk=0
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            return self.objects.filter(account_id=account_id).first()
        if 'luggage_id' in kwargs:
            pk=kwargs['luggage_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class VehicleRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Vehicle.objects
        self.profile=ProfileRepo(*args, **kwargs).me
       
    def add_vehicle(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_vehicle"):
            return
        if 'title' in kwargs:
            title=kwargs['title']
            vehicle=self.vehicle(title=title)
            if vehicle is not None:
                message="عنوان تکراری برای ماشین"
                return None,message
            if vehicle is None and 'plaque' in kwargs:
                vehicle=self.vehicle(plaque=kwargs['plaque'])
                if vehicle is not None:
                    message="پلاک تکراری برای ماشین"
                    return None,message
                    
            if vehicle is None:
                vehicle=Vehicle()
                if 'title' in kwargs:
                    vehicle.title=kwargs['title']
                if 'plaque' in kwargs:
                    vehicle.plaque=kwargs['plaque']
                if 'color' in kwargs:
                    vehicle.color=kwargs['color']
                if 'description' in kwargs:
                    vehicle.description=kwargs['description']
                if 'vehicle_type' in kwargs:
                    vehicle.vehicle_type=kwargs['vehicle_type']
                if 'brand' in kwargs:
                    vehicle.brand_name=kwargs['brand']
                vehicle.save()
                message=""
                return vehicle,message

    def vehicle(self, *args, **kwargs):
        pk=0
        if 'vehicle' in kwargs:
            return kwargs['vehicle']
        if 'title' in kwargs:
            return self.objects.filter(title=kwargs['title']).first()
        if 'plaque' in kwargs:
            return self.objects.filter(plaque=kwargs['plaque']).first()
        if 'vehicle_id' in kwargs:
            return self.objects.filter(pk=kwargs['vehicle_id']).first()
        elif 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        elif 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class TripPathRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=TripPath.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_trip_path(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trippath"):
            return
        trip_path=TripPath()
        if 'source_id' in kwargs:
            trip_path.source_id=kwargs['source_id']
        if 'destination_id' in kwargs:
            trip_path.destination_id=kwargs['destination_id']
        if 'cost' in kwargs:
            trip_path.cost=kwargs['cost']
        if 'distance' in kwargs:
            trip_path.distance=kwargs['distance']
        if 'title' in kwargs:
            trip_path.title=kwargs['title']
        if 'duration' in kwargs:
            trip_path.duration=kwargs['duration']
        if 'area_id' in kwargs:
            trip_path.area_id=kwargs['area_id']
        trip_path.save()
        return trip_path
    
   

    def trip_path(self, *args, **kwargs):
        pk=0
        if 'trip_path_id' in kwargs:
            pk=kwargs['trip_path_id']
        if 'trippath_id' in kwargs:
            pk=kwargs['trippath_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


class TripRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Trip.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def add_trip(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trip"):
            return
        trip=Trip()

        key='pay_to_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_to_id=kwargs[key]

        key='client_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            client=Client.objects.filter(pk=kwargs[key]).first()
            if client is not None:
                trip.pay_to_id=client.account.id

        key='driver_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            driver=Driver.objects.filter(pk=kwargs[key]).first()
            if driver is not None:
                trip.pay_from_id=driver.account.id

        key='pay_from_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_from_id=kwargs[key]

        key='amount'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.amount=kwargs[key]

        key='delay'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.delay=kwargs[key]

        key='description'
        if key in kwargs and kwargs[key] is not None:
            trip.description=kwargs[key]


        key='date_started'
        if key in kwargs and kwargs[key] is not None:
            trip.date_started=kwargs[key]

        key='date_ended'
        if key in kwargs and kwargs[key] is not None:
            trip.date_ended=kwargs[key]


        key='title'
        if key in kwargs and kwargs[key] is not None:
            trip.title=kwargs[key]

        key='vehicle_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.vehicle_id=kwargs[key]



        key='trip_category_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.trip_category_id=kwargs[key] 


        key='duration'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.duration=kwargs[key]
        else:
            trip.duration=0
        key='distance'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.distance=kwargs[key]
        else:
            trip.distance=0

        trip.save()
        
        key='passengers'
        if key in kwargs and kwargs[key] is not None:
            passengers=kwargs[key]
            for passenger_id in passengers:
                trip.passengers.add(passenger_id)

        key='trip_paths'
        if key in kwargs and kwargs[key] is not None:
            trip_paths=kwargs[key]
            for trip_path_id in trip_paths:
                trip.trip_paths.add(trip_path_id)

        trip.save()
        return trip

    def trip(self, *args, **kwargs):
        pk=0
        if 'trip_id' in kwargs:
            pk=kwargs['trip_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'client_id' in kwargs:
            objects=objects.filter(pay_to_id=kwargs['client_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(pay_from_id=kwargs['driver_id'])
        if 'trip_category_id' in kwargs:
            objects=objects.filter(trip_category_id=kwargs['trip_category_id'])
        return objects.all()


class ServiceManRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=ServiceMan.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_service_man(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_serviceman"):
            return
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            service_man=self.service_man(account_id=account_id)

            if service_man is None:
                service_man=ServiceMan(account_id=account_id)
                if 'title' in kwargs:
                    service_man.title=kwargs['title']
                service_man.save()
                return service_man
    def add_work_shift(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trip"):
            return
        trip=Trip()

        key='pay_to_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_to_id=kwargs[key]

        key='pay_from_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_from_id=kwargs[key]

        key='amount'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.amount=kwargs[key]

        key='delay'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.delay=kwargs[key]

        key='description'
        if key in kwargs and kwargs[key] is not None:
            trip.description=kwargs[key]

        key='title'
        if key in kwargs and kwargs[key] is not None:
            trip.title=kwargs[key]

        key='vehicle_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.vehicle_id=kwargs[key]



        key='trip_category_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.trip_category_id=kwargs[key] 


        key='duration'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.duration=kwargs[key]
        else:
            trip.duration=0
        key='distance'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.distance=kwargs[key]
        else:
            trip.distance=0

        trip.save()
        
        key='passengers'
        if key in kwargs and kwargs[key] is not None:
            passengers=kwargs[key]
            for passenger_id in passengers:
                trip.passengers.add(passenger_id)

        key='trip_paths'
        if key in kwargs and kwargs[key] is not None:
            trip_paths=kwargs[key]
            for trip_path_id in trip_paths:
                trip.trip_paths.add(trip_path_id)

        trip.save()
        return trip

    def service_man(self, *args, **kwargs):
        pk=0
        if 'service_man_id' in kwargs:
            pk=kwargs['service_man_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'client_id' in kwargs:
            objects=objects.filter(pay_to_id=kwargs['client_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(pay_from_id=kwargs['driver_id'])
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        return objects.all()


class MaintenanceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Maintenance.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def add_work_shift(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trip"):
            return
        trip=Trip()

        key='pay_to_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_to_id=kwargs[key]

        key='pay_from_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.pay_from_id=kwargs[key]

        key='amount'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.amount=kwargs[key]

        key='delay'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.delay=kwargs[key]

        key='description'
        if key in kwargs and kwargs[key] is not None:
            trip.description=kwargs[key]

        key='title'
        if key in kwargs and kwargs[key] is not None:
            trip.title=kwargs[key]

        key='vehicle_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.vehicle_id=kwargs[key]



        key='trip_category_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.trip_category_id=kwargs[key] 


        key='duration'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.duration=kwargs[key]
        else:
            trip.duration=0
        key='distance'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            trip.distance=kwargs[key]
        else:
            trip.distance=0

        trip.save()
        
        key='passengers'
        if key in kwargs and kwargs[key] is not None:
            passengers=kwargs[key]
            for passenger_id in passengers:
                trip.passengers.add(passenger_id)

        key='trip_paths'
        if key in kwargs and kwargs[key] is not None:
            trip_paths=kwargs[key]
            for trip_path_id in trip_paths:
                trip.trip_paths.add(trip_path_id)

        trip.save()
        return trip

    def maintenance(self, *args, **kwargs):
        pk=0
        if 'maintenance_id' in kwargs:
            pk=kwargs['maintenance_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'client_id' in kwargs:
            objects=objects.filter(pay_to_id=Client.objects.filter(pk=kwargs['client_id']).first().account_id)
        if 'driver_id' in kwargs:
            objects=objects.filter(pay_from_id=kwargs['driver_id'])
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'service_man_id' in kwargs:
            objects=objects.filter(pay_from_id=ServiceMan.objects.filter(pk=kwargs['service_man_id']).first().account_id)
        return objects.all()

    def add_maintenance(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_maintenance"):
            return
        maintenance=Maintenance()
        if 'amount' in kwargs:
            maintenance.amount=kwargs['amount']
        if 'title' in kwargs:
            maintenance.title=kwargs['title']
        if 'kilometer' in kwargs:
            maintenance.kilometer=kwargs['kilometer']
        if 'description' in kwargs:
            maintenance.description=kwargs['description']
        if 'event_datetime' in kwargs:
            maintenance.transaction_datetime=kwargs['event_datetime']
        if 'maintenance_type' in kwargs:
            maintenance.maintenance_type=kwargs['maintenance_type']
        if 'service_man_id' in kwargs:
            maintenance.pay_from_id=ServiceMan.objects.filter(pk=kwargs['service_man_id']).first().account_id
        if 'client_id' in kwargs:
            maintenance.pay_to_id=Client.objects.filter(pk=kwargs['client_id']).first().account_id
        if 'vehicle_id' in kwargs:
            maintenance.vehicle_id=kwargs['vehicle_id']
        if 'status' in kwargs:
            maintenance.status=kwargs['status']
        if 'payment_method' in kwargs:
            maintenance.payment_method=kwargs['payment_method']
        maintenance.save()
        return maintenance


class WorkShiftRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=WorkShift.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def add_work_shift(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_workshift"):
            return
        work_shift=WorkShift()

        key='pay_to_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.pay_to_id=kwargs[key]

        key='pay_from_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.pay_from_id=kwargs[key]

        key='amount'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.amount=kwargs[key]

        key='vehicle_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.vehicle_id=kwargs[key]
        
        key='driver_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.driver_id=kwargs[key]

        key='area_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.area_id=kwargs[key]

        key='description'
        if key in kwargs and kwargs[key] is not None:
            work_shift.description=kwargs[key]

        key='start_datetime'
        if key in kwargs and kwargs[key] is not None:
            work_shift.start_datetime=kwargs[key]

        key='end_datetime'
        if key in kwargs and kwargs[key] is not None:
            work_shift.end_datetime=kwargs[key]
            work_shift.transaction_datetime=kwargs[key]

        key='title'
        if key in kwargs and kwargs[key] is not None:
            work_shift.title=kwargs[key]

        key='trip_category_id'
        if key in kwargs and kwargs[key] is not None and kwargs[key]>0:
            work_shift.trip_category_id=kwargs[key] 


        

        work_shift.save()
       
        return work_shift

    def work_shift(self, *args, **kwargs):
        pk=0
        if 'work_shift_id' in kwargs:
            pk=kwargs['work_shift_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'client_id' in kwargs:
            objects=objects.filter(pay_to_id=kwargs['client_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(pay_from_id=kwargs['driver_id'])
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        return objects.all()


class PassengerRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Passenger.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def add_passenger(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_passenger"):
            return
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            passenger=self.passenger(account_id=account_id)

            if passenger is None:
                passenger=Passenger(account_id=account_id)
                if 'title' in kwargs:
                    passenger.title=kwargs['title']
                passenger.save()
                return passenger


    def passenger(self, *args, **kwargs):
        pk=0
        if 'passenger_id' in kwargs:
            pk=kwargs['passenger_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

   
class ClientRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Client.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def add_client(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_passenger"):
            return
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            client=self.client(account_id=account_id)

            if client is None:
                client=Client(account_id=account_id)
                if 'title' in kwargs and kwargs['title'] is not None and not kwargs['title']=="":
                    client.title=kwargs['title']
                client.save()
                return client

    def client(self, *args, **kwargs):
        pk=0
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            return self.objects.filter(account_id=account_id).first()
        if 'client_id' in kwargs:
            pk=kwargs['client_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

   
class TripCategoryRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=TripCategory.objects.order_by('title')
        self.profile=ProfileRepo(*args, **kwargs).me
    def add_trip_category(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_tripcategory"):
            return
        if 'title' in kwargs:
            title=kwargs['title']
            trip_category=self.trip_category(title=title)


            if trip_category is None:
                trip_category=TripCategory(title=title)
                if 'color' in kwargs:
                    trip_category.color=kwargs['color']
                trip_category.save()
                return trip_category

    def trip_category(self, *args, **kwargs):
        pk=0
        if 'title' in kwargs:
            title=kwargs['title']
            return self.objects.filter(title=title).first()
        if 'trip_category_id' in kwargs:
            pk=kwargs['trip_category_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

   

