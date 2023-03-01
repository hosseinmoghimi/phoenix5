from core.enums import ColorEnum
from utility.calendar import to_persian_month_name
from utility.currency import to_price
from django.db import models
from salary.enums import *
from salary.apps import APP_NAME
from core.models import _,reverse,Page,LinkHelper
from utility.calendar import to_persian_datetime_tag
from utility.calendar import PersianCalendar,PERSIAN_MONTH_NAMES


class DailyAttendance(models.Model,LinkHelper):
    employee = models.ForeignKey("organization.employee", verbose_name=_(
        "پرسنل"), on_delete=models.CASCADE)
    attendance_date=models.DateField(_("تاریخ"), auto_now=False, auto_now_add=False)
    delay=models.IntegerField(_("تاخیر"),default=0)
    hurry=models.IntegerField(_("تعجیل"),default=0)
    leave=models.IntegerField(_("مرخصی"),default=0)
    rest=models.IntegerField(_("استراحت"),default=0)
    duration=models.IntegerField(_("دقایق حضور"),default=0)
    status=models.CharField(_("وضعیت"),max_length=100,choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.NOT_SET,)
    date_registered=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=False)
    
    class_name="dailyattendance"
    app_name=APP_NAME
                               
    
    def __str__(self):
        # return self.title
        return f"{self.employee.title} @ {PersianCalendar().from_gregorian(self.attendance_date,only_date=True)}"

    class Meta:
        verbose_name = _("DailyAttendance")
        verbose_name_plural = _("DailyAttendances")

    def save(self, *args, **kwargs):
        return super(DailyAttendance, self).save(*args, **kwargs)
    
   
class MonthlyAttendance(models.Model,LinkHelper):
    employee = models.ForeignKey("organization.employee", verbose_name=_(
        "پرسنل"), on_delete=models.CASCADE)

    month=models.IntegerField(_("ماه"),default=0)
    year=models.IntegerField(_("سال"),default=0)

    delay=models.IntegerField(_("تاخیر"),default=0)
    hurry=models.IntegerField(_("تعجیل"),default=0)
    leave=models.IntegerField(_("مرخصی"),default=0)
    rest=models.IntegerField(_("استراحت"),default=0)
    duration=models.IntegerField(_("دقایق حضور"),default=0)
    status=models.CharField(_("وضعیت"),max_length=100,choices=AttendanceStatusEnum.choices,default=AttendanceStatusEnum.NOT_SET,)
    date_registered=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=False)
    
    class_name="monthlyattendance"
    app_name=APP_NAME
                               
    
    def __str__(self):
        # return self.title
        return f"{self.employee.title} @ {PERSIAN_MONTH_NAMES[self.month]} {self.year}"

    class Meta:
        verbose_name = _("MonthlyAttendance")
        verbose_name_plural = _("MonthlyAttendances")

    def save(self, *args, **kwargs):
        return super(MonthlyAttendance, self).save(*args, **kwargs)
    
   
class Group(models.Model,LinkHelper):
    title=models.CharField(_("عنوان"),max_length=100)
    type=models.CharField(_("نوع"),max_length=100,choices=GroupTypeEnum.choices,default=GroupTypeEnum.EMPLOYEE,)
    description=models.CharField(_("توضیحات"),null=True,blank=True,max_length=100)
    employees=models.ManyToManyField("organization.employee",blank=True, verbose_name=_("پرسنل"))
    rows=models.ManyToManyField("salaryitem",blank=True, verbose_name=_("آیتم"))
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
    title=models.CharField(_("عنوان"), max_length=50)
    amount=models.IntegerField(_("مبلغ"))
    direction=models.CharField(_("جهت"),choices=SalaryRowDirectionEnum.choices,default=SalaryRowDirectionEnum.MAZAYA, max_length=50)
    class Meta:
        verbose_name = _("SalaryItem")
        verbose_name_plural = _("SalaryItems")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("SalaryRow_detail", kwargs={"pk": self.pk})


class Salary(models.Model,LinkHelper):
    employee=models.ForeignKey("organization.employee", verbose_name=_("پرسنل"), on_delete=models.CASCADE)
    title=models.CharField(_("عنوان"), max_length=50)
    amount=models.IntegerField(_("مبلغ"))
    month=models.IntegerField(_("ماه"))
    year=models.IntegerField(_("سال"))
    direction=models.CharField(_("جهت"),choices=SalaryRowDirectionEnum.choices,default=SalaryRowDirectionEnum.MAZAYA, max_length=50)
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=500)

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
 

class TimeTable(models.Model,LinkHelper):
    title=models.CharField(_("عنوان"), max_length=50)
    start_time=models.TimeField(_("شروع"), auto_now=False, auto_now_add=False)
    end_time=models.TimeField(_("پایان"), auto_now=False, auto_now_add=False)
    enter_start_time=models.TimeField(_("شروع ورود"), auto_now=False, auto_now_add=False)
    enter_end_time=models.TimeField(_("پایان ورود"), auto_now=False, auto_now_add=False)
    exit_start_time=models.TimeField(_("شروع خروج"), auto_now=False, auto_now_add=False)
    exit_end_time=models.TimeField(_("پایان خروج"), auto_now=False, auto_now_add=False)
    enter_delay=models.IntegerField(_("تاخیر ورود"),default=0)
    exit_hurry=models.IntegerField(_("تعجیل خروج"),default=0)
    day_count=models.IntegerField(_("روز کاری"),default=1)
    rest_start=models.TimeField(_("شروع استراحت"), auto_now=False, auto_now_add=False)
    rest_end=models.TimeField(_("پایان استراحت"), auto_now=False, auto_now_add=False)
    color=models.CharField(_("رنگ") , choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    @property
    def minutes(self):
        return 0
    class_name="timetable"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("TimeTable")
        verbose_name_plural = _("TimeTables")

    def __str__(self):
        return self.title
 

class WorkShift(models.Model,LinkHelper):
    title=models.CharField(_("عنوان"), max_length=50)
    time_tables=models.ManyToManyField("timetable", verbose_name=_("جدول های زمانی"))
    saturday=models.BooleanField(_("شنبه"))
    sunday=models.BooleanField(_("یکشنبه"))
    monday=models.BooleanField(_("دوشنبه"))
    tuesday=models.BooleanField(_("سه شنبه"))
    wednesday=models.BooleanField(_("چهار شنبه"))
    thursday=models.BooleanField(_("پنج شنبه"))
    friday=models.BooleanField(_("جمعه"))
    app_name=APP_NAME
    class_name="workshift"
    class Meta:
        verbose_name = _("WorkShift")
        verbose_name_plural = _("WorkShifts")

    def __str__(self):
        return self.title
 

class EmployeeTiming(models.Model,LinkHelper):
    app_name=APP_NAME
    class_name="employeetiming"
    employee=models.ForeignKey("organization.employee", verbose_name=_("پرسنل"), on_delete=models.CASCADE)
    work_shifts=models.ManyToManyField("workshift", verbose_name=_("workshifts"))
    

    class Meta:
        verbose_name = _("EmployeeTiming")
        verbose_name_plural = _("EmployeeTimings")

    def __str__(self):
        return f"{self.employee.title} "
 

class EmployeeCross(models.Model,LinkHelper):
    class_name="employeecross"
    app_name=APP_NAME
    employee=models.ForeignKey("organization.employee", verbose_name=_("پرسنل"), on_delete=models.CASCADE)
    type=models.CharField(_("نوع تردد"),choices=CrossTypeEnum.choices, max_length=50)
    cross_datetime=models.DateTimeField(_("تاریخ و ساعت"), auto_now=False, auto_now_add=False)
    

    class Meta:
        verbose_name = _("EmployeeCross")
        verbose_name_plural = _("EmployeeCrosss")

    def __str__(self):
        return f"{self.employee} @ {PersianCalendar().from_gregorian(self.cross_datetime)}"

    def get_absolute_url(self):
        return reverse("EmployeeCross_detail", kwargs={"pk": self.pk})
