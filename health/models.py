from email.policy import default
from django.db import models
from core.enums import ColorEnum
from core.models import _,reverse,Page,LinkHelper
from health.apps import APP_NAME
from health.enums import *
from utility.calendar import PersianCalendar, to_persian_datetime_tag


class Drug(Page):
  
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name == "":
            self.class_name = "drug"
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        return super(Drug,self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")
 

# class Disease(Page):
#     drugs=models.ManyToManyField("drug",blank=True, verbose_name=_("drugs"))
#     level=models.IntegerField(_("level"))
#     color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
   
#     def save(self,*args, **kwargs):
#         if self.class_name is None or self.class_name == "":
#             self.class_name = "disease"
#         if self.app_name is None or self.app_name == "":
#             self.app_name = APP_NAME
#         return super(Disease,self).save(*args, **kwargs)
    

#     class Meta:
#         verbose_name = _("Disease")
#         verbose_name_plural = _("Diseases")
 

class Patient(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="patient"
    app_name=APP_NAME
    
    def __str__(self):
        return self.account.title

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
 

class Doctor(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="doctor"
    app_name=APP_NAME
    
    def __str__(self):
        return self.account.title

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class Disease(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    drugs=models.ManyToManyField("drug",blank=True, verbose_name=_("drugs"))
    level=models.IntegerField(_("level"),default=1)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    app_name=APP_NAME
    class_name="disease"
    

    class Meta:
        verbose_name = _("Disease")
        verbose_name_plural = _("Diseases")

    def __str__(self):
        return self.name
 

class Visit(models.Model,LinkHelper):
    app_name=APP_NAME
    class_name="visit"
    visit_datetime=models.DateTimeField(_("visit"), auto_now=False, auto_now_add=False)
    patient=models.ForeignKey("patient", verbose_name=_("patient"), on_delete=models.CASCADE)
    doctor=models.ForeignKey("doctor", verbose_name=_("doctor"), on_delete=models.CASCADE)
    diseases=models.ManyToManyField("disease",blank=True, verbose_name=_("diseases"))
    drugs=models.ManyToManyField("drug",blank=True, verbose_name=_("drug"))
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    class Meta:
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")
    def persian_visit_datetime(self):
        return PersianCalendar().from_gregorian(self.visit_datetime)
    def persian_visitdatetime_tag(self):
        return to_persian_datetime_tag(self.visit_datetime)
    def __str__(self):
        return f"{self.doctor}@{self.patient}@{self.persian_visit_datetime()}"
 