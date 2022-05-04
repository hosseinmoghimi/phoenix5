from django.db import models
from attendance.enums import AttendanceStatusEnum
from attendance.apps import APP_NAME
from core.models import _,reverse,Page,LinkHelper
from utility.calendar import to_persian_datetime_tag

class Attendance(models.Model,LinkHelper):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    delay=models.IntegerField(_("delay"),default=0)
    status=models.CharField(_("status"),choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.NOT_SET,)
    date_registered=models.DateTimeField(_("date_registered"), auto_now=False, auto_now_add=False)
    
    class_name="attendance"
    app_name=APP_NAME
                               
    
    def __str__(self):
        # return self.title
        return self.profile.name

    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("رکورد حضور و غیاب")

    def save(self, *args, **kwargs):
        return super(Attendance, self).save(*args, **kwargs)
    
      