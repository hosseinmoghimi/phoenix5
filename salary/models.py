from utility.calendar import to_persian_month_name
from utility.currency import to_price
from django.db import models
from salary.enums import *
from salary.apps import APP_NAME
from core.models import _,reverse,Page,LinkHelper
from utility.calendar import to_persian_datetime_tag

class Attendance(models.Model,LinkHelper):
    account = models.ForeignKey("accounting.account", verbose_name=_(
        "account"), on_delete=models.CASCADE)
    delay=models.IntegerField(_("delay"),default=0)
    status=models.CharField(_("status"),max_length=100,choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.NOT_SET,)
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
    

    
class Group(models.Model,LinkHelper):
    title=models.CharField(_("title"),max_length=100)
    type=models.CharField(_("type"),max_length=100,choices=GroupTypeEnum.choices,default=GroupTypeEnum.EMPLOYEE,)
    description=models.CharField(_("description"),null=True,blank=True,max_length=100)
    employees=models.ManyToManyField("organization.employee",blank=True, verbose_name=_("employees"))
    rows=models.ManyToManyField("salaryitem",blank=True, verbose_name=_("item"))
    class_name="group"
    app_name=APP_NAME
                               
    
    def __str__(self):
        # return self.title
        return self.title

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def save(self, *args, **kwargs):
        return super(Group, self).save(*args, **kwargs)
 


class SalaryItem(models.Model):
    title=models.CharField(_("title"), max_length=50)
    amount=models.IntegerField(_("amount"))
    direction=models.CharField(_("direction"),choices=SalaryRowDirectionEnum.choices,default=SalaryRowDirectionEnum.MAZAYA, max_length=50)
    class Meta:
        verbose_name = _("SalaryItem")
        verbose_name_plural = _("SalaryItems")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("SalaryRow_detail", kwargs={"pk": self.pk})


class Salary(models.Model,LinkHelper):
    employee=models.ForeignKey("organization.employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    amount=models.IntegerField(_("amount"))
    month=models.IntegerField(_("month"))
    year=models.IntegerField(_("year"))
    direction=models.CharField(_("direction"),choices=SalaryRowDirectionEnum.choices,default=SalaryRowDirectionEnum.MAZAYA, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)

    app_name=APP_NAME
    class_name="salary"
    class Meta:
        verbose_name = _("Salary")
        verbose_name_plural = _("Salarys")
    @property
    def color(self):
        if self.direction==SalaryRowDirectionEnum.MAZAYA:
            return "success"
        return "danger"
    @property
    def month_name(self):
        return to_persian_month_name(self.month)


    def __str__(self):
        return f"{self.employee.title} {self.year}/{self.month} : {self.title}  = {to_price(self.amount)}"
 