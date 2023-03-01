from django.contrib import admin

from salary.models import DailyAttendance,MonthlyAttendance,Group,SalaryItem,Salary,TimeTable,WorkShift,EmployeeTiming,EmployeeCross

# Register your models here.
admin.site.register(Group)
admin.site.register(DailyAttendance)
admin.site.register(MonthlyAttendance)
admin.site.register(TimeTable)
admin.site.register(Salary)
admin.site.register(SalaryItem)
admin.site.register(WorkShift)
admin.site.register(EmployeeCross)
admin.site.register(EmployeeTiming)