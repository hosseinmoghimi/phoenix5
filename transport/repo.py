from transport.apps import APP_NAME
from .models import Driver, Maintenance,Passenger,ServiceMan, Trip, TripCategory, TripPath, Vehicle,Client, WorkShift
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
       

    def vehicle(self, *args, **kwargs):
        pk=0
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
            objects=objects.filter(pay_to_id=kwargs['client_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(pay_from_id=kwargs['driver_id'])
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        return objects.all()


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

        key='description'
        if key in kwargs and kwargs[key] is not None:
            work_shift.description=kwargs[key]

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
       

    def client(self, *args, **kwargs):
        pk=0
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
        
        self.objects=TripCategory.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def trip_category(self, *args, **kwargs):
        pk=0
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

   

