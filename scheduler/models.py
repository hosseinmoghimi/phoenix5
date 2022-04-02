from django.db import models
from scheduler.apps import APP_NAME
from core.models import LinkHelper,Page,_
from utility.calendar import to_persian_datetime_tag

class Appointment(Page):

    profiles=models.ManyToManyField("authentication.profile",related_name="appointments",blank=True, verbose_name=_("profiles"))
    date_fixed=models.DateTimeField(_("date_fixed"), auto_now=False, auto_now_add=False)
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
