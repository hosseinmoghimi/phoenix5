from accounting.models import Asset
from utility.calendar import PERSIAN_MONTH_NAMES, PersianCalendar
from core.middleware import get_request
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


class Driver(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    color=models.CharField(_("color"),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    class_name='driver'
    app_name=APP_NAME
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
    def __str__(self):
        return self.profile.name


class Passenger(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name="passenger"
    app_name=APP_NAME

    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'vehicle_id':0,'passenger_id':self.pk,'trip_path_id':0})
    
    class Meta:
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.profile.name


class Area(models.Model,LinkHelper):
    code=models.CharField(_("code"), max_length=50)
    name=models.CharField(_("area"), max_length=50)
    app_name=APP_NAME
    class_name="area"
    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.name



class ServiceMan(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    name=models.CharField(_("نام تعمیرگاه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    
    app_name=APP_NAME
    class_name="serviceman"
    class Meta:
        verbose_name = _("ServiceMan")
        verbose_name_plural = _("ServiceMans")

    def __str__(self):
        return self.name if self.name is not None else self.profile.name
 

class Vehicle(Asset):
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.SEDAN, max_length=50)
    brand=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.TOYOTA, max_length=50)
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

class WorkShift(models.Model,LinkHelper):
    area=models.ForeignKey("area", verbose_name=_("area"), on_delete=models.CASCADE)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)
    driver=models.ForeignKey("driver", verbose_name=_("driver"), on_delete=models.CASCADE)
    start_time=models.DateTimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    income=models.IntegerField(_("درآمد"),default=0)
    outcome=models.IntegerField(_("هزینه"),default=0)
    description=models.CharField(_("توضیحات"), null=True,blank=True,max_length=500)
    class_name="workshift"
    app_name=APP_NAME
    def persian_start_time(self):
        return PersianCalendar().from_gregorian(self.start_time)
    def persian_end_time(self):
        return PersianCalendar().from_gregorian(self.end_time)
    class Meta:
        verbose_name = _("WorkShift")
        verbose_name_plural = _("WorkShifts")

    def __str__(self):
        return f'{self.vehicle.title} {self.persian_start_time()}'

  



 

class TripPath(models.Model,LinkHelper):
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
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    class_name="tripcategory"
    app_name=APP_NAME
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
 
class Trip(models.Model,LinkHelper):
    status=models.CharField(_("status"), choices=TripStatusEnum.choices,default=TripStatusEnum.REQUESTED, max_length=50)
    title=models.CharField(_("title"), max_length=200)
    category=models.ForeignKey("tripcategory",null=True,blank=True, verbose_name=_("نوع سفر"), on_delete=models.SET_NULL)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)
    driver=models.ForeignKey("driver", verbose_name=_("driver"), on_delete=models.CASCADE)
    distance=models.IntegerField(_("distance"),default=5)
    cost=models.IntegerField(_("cost"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_started=models.DateTimeField(_("شروع سرویس"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_ended=models.DateTimeField(_("پایان سرویس"),null=True,blank=True, auto_now=False, auto_now_add=False)
    paths=models.ManyToManyField("trippath",blank=True, verbose_name=_("مسیر های سرویس"))
    passengers=models.ManyToManyField("passenger",blank=True, verbose_name=_("مسافر ها"))
    delay=models.IntegerField(_("تاخیر"),default=0)
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=5000)
    class_name="trip"
    app_name=APP_NAME
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
  


  
class VehicleEvent(Page):
    # title=models.CharField(_("title"),blank=True, max_length=50)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("ماشین"), on_delete=models.CASCADE)
    event_datetime=models.DateTimeField(_("event_datetime"), auto_now=False, auto_now_add=False)
    kilometer=models.IntegerField(_("کارکرد"),null=True,blank=True)

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


class Maintenance(VehicleEvent,LinkHelper):
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceEnum.choices, max_length=100)
    service_man=models.ForeignKey("serviceman", verbose_name=_("سرویس کار"),null=True,blank=True, on_delete=models.CASCADE)
    paid=models.IntegerField(_("هزینه به تومان"))
 
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
 
class VehicleWorkEvent(VehicleEvent,LinkHelper):
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
 