from django.contrib import admin

from salary.models import Attendance,Group,SalaryItem,Salary

# Register your models here.
admin.site.register(Group)
admin.site.register(Attendance)
admin.site.register(Salary)
admin.site.register(SalaryItem)