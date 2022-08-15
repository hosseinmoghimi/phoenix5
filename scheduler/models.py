from django.db import models
from core.enums import ColorEnum
from scheduler.apps import APP_NAME
from core.models import LinkHelper,Page,_
from scheduler.enums import *
from utility.calendar import to_persian_datetime_tag

class Appointment(Page):
    accounts=models.ManyToManyField("accounting.account",blank=True, verbose_name=_("accounts"))
    profiles=models.ManyToManyField("authentication.profile",related_name="appointments",blank=True, verbose_name=_("profiles"))
    date_fixed=models.DateTimeField(_("date_fixed"), auto_now=False, auto_now_add=False)
    status=models.CharField(_("status"),choices=AppointmentStatusEnum.choices,default=AppointmentStatusEnum.DRAFT, max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    def persian_date_fixed(self):
        return to_persian_datetime_tag(self.date_fixed)
    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
 
    def locations(self):
        return (pagelocation.location for pagelocation in self.pagelocation_set.all())
    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.class_name is None:
            self.class_name='appointment'
        super(Appointment,self).save(*args, **kwargs)

    def status_color(self):
        badge_color=ColorEnum.PRIMARY
        if self.status==AppointmentStatusEnum.DONE:
            badge_color=ColorEnum.PRIMARY
        if self.status==AppointmentStatusEnum.CANCELED:
            badge_color=ColorEnum.SECONDARY
        if self.status==AppointmentStatusEnum.APPROVED:
            badge_color=ColorEnum.SUCCESS
        if self.status==AppointmentStatusEnum.DONE:
            badge_color=ColorEnum.PRIMARY
        return badge_color