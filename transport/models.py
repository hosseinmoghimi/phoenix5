from accounting.models import Asset, Transaction
from utility.calendar import PERSIAN_MONTH_NAMES, PersianCalendar, to_persian_datetime_tag
from phoenix.settings import STATIC_URL
from django.db import models
from core.models import  Page
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.utils import LinkHelper
from .enums import *
from tinymce.models import HTMLField
from core.enums import ColorEnum,UnitNameEnum
from accounting.models import Account


class Driver(models.Model,LinkHelper):
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name='driver'
    app_name=APP_NAME
    color=models.CharField(_("color"),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers' 

    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.account.title
        return super(Driver,self).save(*args, **kwargs)
    def __str__(self):
        return str(self.title)


class Passenger(models.Model,LinkHelper):
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name='passenger'
    app_name=APP_NAME

    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'vehicle_id':0,'passenger_id':self.pk,'trip_path_id':0})
    
    class Meta:
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")
 
    def save(self,*args, **kwargs): 
        if self.title is None or self.title=="":
            self.title=self.account.title
        return super(Passenger,self).save(*args, **kwargs)


    def __str__(self):
        return str(self.title)


class Client(models.Model,LinkHelper):
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name='client'
    app_name=APP_NAME
    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'vehicle_id':0,'passenger_id':self.pk,'trip_path_id':0})
    
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Client")
 
    def save(self,*args, **kwargs):
       
        if self.title is None or self.title=="":
            self.title=self.account.title
        return super(Client,self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class ServiceMan(models.Model,LinkHelper):
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name='serviceman'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("ServiceMan")
        verbose_name_plural = _("ServiceMans")

    def __str__(self):
        return str(self.title)
    def save(self,*args, **kwargs):
       
        if self.title is None or self.title=="":
            self.title=self.account.title
        return super(ServiceMan,self).save(*args, **kwargs)


class Vehicle(Asset):
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.SEDAN, max_length=50)
    brand=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.IRAN_KHODRO, max_length=50)
    model_name=models.CharField(_("مدل"),null=True,blank=True, max_length=50)
    plaque=models.CharField(_("پلاک"),null=True,blank=True, max_length=50)
    driver=models.CharField(_("راننده"), max_length=50,null=True,blank=True)
    color=models.CharField(_("رنگ"),choices=VehicleColorEnum.choices,default=VehicleColorEnum.SEFID, max_length=50)

    kilometer=models.IntegerField(_("کیلومتر"),default=0)
    def save(self,*args, **kwargs):
        self.class_name="vehicle"
        self.app_name=APP_NAME
        return super(Vehicle,self).save(*args, **kwargs)
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'passenger_id':0,'vehicle_id':self.pk,'trip_path_id':0})
      

    def thumbnail(self):
        pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRAILER:
            pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRUCK:
            pic='truck.jpg'
        if self.vehicle_type==VehicleTypeEnum.TAXI:
            pic='taxi.jpg'
        if self.vehicle_type==VehicleTypeEnum.LOADER:
            pic='loader.jpg'
        if self.vehicle_type==VehicleTypeEnum.SEDAN:
            pic='sedan.jpg'
        if self.vehicle_type==VehicleTypeEnum.BUS:
            pic='bus.jpg'
        if self.vehicle_type==VehicleTypeEnum.GRADER:
            pic='grader.jpg'
        return f'{STATIC_URL}{APP_NAME}/images/thumbnail/{pic}/' 


class WorkShift(Transaction):
    area=models.ForeignKey("map.area", verbose_name=_("area"), on_delete=models.CASCADE)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)
    driver=models.ForeignKey("driver", verbose_name=_("driver"), on_delete=models.CASCADE)
    start_time=models.DateTimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    wage=models.IntegerField(_("اجرت راننده"),default=0)
     
    
    @property
    def income(self):
        return self.amount
    @property
    def outcome(self):
        return self.wage

    def persian_start_time(self):
        return to_persian_datetime_tag(self.start_time)
    def persian_end_time(self):
        return to_persian_datetime_tag(self.end_time)
    class Meta:
        verbose_name = _("WorkShift")
        verbose_name_plural = _("WorkShifts")
 
    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=f"شیفت کاری {self.vehicle.title} توسط {self.driver.title} "
        if self.class_name is None or self.class_name=="":
            self.class_name='workshift'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(WorkShift,self).save(*args, **kwargs)


class TripPath(models.Model,LinkHelper):
    area=models.ForeignKey("map.area", null=True,blank=True, verbose_name=_("area"), on_delete=models.CASCADE)
    source=models.ForeignKey("map.location",related_name="trip_source_set", verbose_name=_("مبدا"), on_delete=models.CASCADE)
    destination=models.ForeignKey("map.location",related_name="trip_destination_set", verbose_name=_("مقصد"), on_delete=models.CASCADE)
    cost=models.IntegerField(_("هزینه"),default=0)
    distance=models.IntegerField(_("فاصله"),default=0)
    duration=models.IntegerField(_("مدت زمان تقریبی"),default=0)
    class_name="trippath"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("TripPath")
        verbose_name_plural = _("TripPaths")
    @property
    def title(self):
        return f"مسیر {self.source} به {self.destination}"
    def __str__(self):
        return self.title
    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'passenger_id':0,'vehicle_id':0,'trip_path_id':self.pk})
     

class TripCategory(models.Model,LinkHelper):
    title=models.CharField(_("عنوان"), max_length=50)
    color=models.CharField(_("رنگ"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    class_name="tripcategory"
    app_name=APP_NAME
    def count_of_trips(self):
        return len(self.trip_set.all())
    def get_badge(self):
        return f"""
            <span class="badge badge-{self.color}">{self.title}</span>
        """
    
    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':self.pk,'driver_id':0,'passenger_id':0,'vehicle_id':0,'trip_path_id':0})
    class Meta:
        verbose_name = _("TripCategory")
        verbose_name_plural = _("TripCategorys")

    def __str__(self):
        return self.title
 
 
class Trip(Transaction):
    trip_category=models.ForeignKey("tripcategory",null=True,blank=True, verbose_name=_("نوع سفر"), on_delete=models.SET_NULL)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)
    distance=models.IntegerField(_("distance"))
    duration=models.IntegerField(_("duration"))
    date_started=models.DateTimeField(_("شروع سرویس"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_ended=models.DateTimeField(_("پایان سرویس"),null=True,blank=True, auto_now=False, auto_now_add=False)
    trip_paths=models.ManyToManyField("trippath",blank=True, verbose_name=_("مسیر های سرویس"))
    passengers=models.ManyToManyField("passenger",blank=True, verbose_name=_("مسافر ها"))
    delay=models.IntegerField(_("تاخیر"),default=0)
    
    def persian_date_started(self):
        return to_persian_datetime_tag(self.date_started)
    def persian_date_ended(self):
        return to_persian_datetime_tag(self.date_ended)

    @property
    def driver(self):
        return Driver.objects.filter(account_id=self.pay_from.id).first()
    @property
    def client(self):
        return Client.objects.filter(account_id=self.pay_to.id).first()
    @property
    def cost(self):
        return self.amount
    def get_status_color(self):
        color="primary"
        if self.status==TripStatusEnum.REQUESTED:
            color="danger"
        if self.status==TripStatusEnum.CANCELED:
            color="secondary"
        if self.status==TripStatusEnum.APPROVED:
            color="primary"
        if self.status==TripStatusEnum.DELIVERED:
            color="success"
        return color

    def persian_date_started(self):
        return PersianCalendar().from_gregorian(self.date_started)
    def persian_date_ended(self):
        return PersianCalendar().from_gregorian(self.date_ended)

    class Meta:
        verbose_name = _("Trip")
        verbose_name_plural = _("Trips")

    def __str__(self):
        return self.title
  

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='trip'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        duration=0
        distance=0
        super(Trip,self).save(*args, **kwargs)

        if self.distance==0 or self.duration==0:
            for trip_path in self.trip_paths.all():
                distance+=trip_path.distance
                duration+=trip_path.duration
            if self.distance==0:
                self.distance=distance
            if self.duration==0:
                self.duration=duration
                super(Trip,self).save(*args, **kwargs)

  
class VehicleEvent(Transaction):
    # title=models.CharField(_("title"),blank=True, max_length=50)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("ماشین"), on_delete=models.CASCADE)
    kilometer=models.IntegerField(_("کارکرد"),null=True,blank=True)
    @property
    def event_datetime(self):
        return self.transaction_datetime
    # description=models.CharField(_("توضیحات"), null=True,blank=True,max_length=500)
    # child_class=models.CharField(_("child_class"),default='vehicleworkevent', max_length=50)
    # images=models.ManyToManyField("core.galleryphoto",blank=True, verbose_name=_("images"))
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='vehicleevent'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(VehicleEvent,self).save(*args, **kwargs)
    def child_object(self):
        if self.child_class=="vehicleworkevent":
            return VehicleWorkEvent.objects.get(pk=self.pk)
        if self.child_class=="maintenance":
            return Maintenance.objects.get(pk=self.pk)
    class Meta:
        verbose_name = 'VehicleEvent'
        verbose_name_plural = 'VehicleEvents'
    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)


class Maintenance(VehicleEvent):
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceEnum.choices, max_length=100)
    @property
    def paid(self):
        return self.amount
    @property
    def service_man(self):
        return ServiceMan.objects.filter(pk=self.pay_from.pk).first()
    def get_icon(self):
        icon="settings"
        color="primary"
        if self.maintenance_type==MaintenanceEnum.NEW_AIR_FILTER:
            icon="luggage"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_OIL_FILTER:
            icon="luggage"
            color='warning'
        if self.maintenance_type==MaintenanceEnum.REPAIR_GEARBOX:
            icon="build"
            color='primary'
        if self.maintenance_type==MaintenanceEnum.REPAIR_ENGINE:
            icon="build"
            color='danger'
        if self.maintenance_type==MaintenanceEnum.NEW_FUEL:
            icon="local_gas_station"
            color='danger'
        if self.maintenance_type==MaintenanceEnum.NEW_INSURANCE:
            icon="addchart"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_TIRE:
            icon="panorama_fish_eye"
            color='primary'
        if self.maintenance_type==MaintenanceEnum.NEW_WATER:
            icon="invert_colors"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_OIL:
            icon="opacity"
            color='warning'
        if self.maintenance_type==MaintenanceEnum.NEW_GLASS:
            icon="window"
            icon="info"
        if self.maintenance_type==MaintenanceEnum.WASH:
            icon="shower"
            color="primary"
        # icon_tag= f'<i class="material-icons">window</i>'
        return {'icon':icon,'color':color}
    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")
    def save(self,*args, **kwargs):
        self.title=self.maintenance_type
        if self.class_name is None or self.class_name=="":
            self.class_name='maintenance'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Maintenance,self).save(*args, **kwargs)

        return super(Maintenance,self).save()
    def __str__(self):
        return f'{self.service_man} {self.maintenance_type} {self.vehicle}'
 

class VehicleWorkEvent(VehicleEvent):
    work_shift=models.ForeignKey("workshift", verbose_name=_("شیفت کاری"), on_delete=models.CASCADE)
    event_type=models.CharField(_("event_type"),choices=WorkEventEnum.choices, max_length=50)
    def get_icon(self):
        icon="settings"
        color="primary"
        if self.event_type==WorkEventEnum.BROKEN_GLASS:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.FLAT_TIRE:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.CRASH1:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.CRASH2:
            icon="luggage"
            color='info'
        
        # icon_tag= f'<i class="material-icons">window</i>'
        return {'icon':icon,'color':color}
    
    def save(self):
        self.title=self.event_type
        if self.class_name is None or self.class_name=="":
            self.class_name='vehicleworkevent'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(VehicleWorkEvent,self).save()
    class Meta:
        verbose_name = _("VehicleWorkEvent")
        verbose_name_plural = _("VehicleWorkEvents")

    def __str__(self):
        return f'{self.work_shift} {self.event_type}'
 