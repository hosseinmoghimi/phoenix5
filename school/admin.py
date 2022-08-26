from django.contrib import admin

from school.models import ActiveCourse, Attendance, Book, ClassRoom, Course, EducationalYear, Exam, Major, Option, Question, School, Session, Student, Teacher
admin.site.register(School)
admin.site.register(Attendance)
admin.site.register(Session)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(EducationalYear)
admin.site.register(ClassRoom)
admin.site.register(Book)
admin.site.register(Exam)
admin.site.register(Course)
admin.site.register(Major)
admin.site.register(ActiveCourse)
# Register your models here.
