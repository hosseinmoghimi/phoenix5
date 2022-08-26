# Create your models here.

from tinymce.models import HTMLField
from core.models import Page, PageLink
from django.db import models
from django.shortcuts import reverse
from phoenix.settings import ADMIN_URL, STATIC_URL
from utility.calendar import PersianCalendar
from school.apps import APP_NAME
from django.utils.translation import gettext as _
from school.settings import *
from school.enums import *
from library.models import Book as LibraryBook
from utility.utils import LinkHelper


class SchoolPage(Page,LinkHelper):

    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME
        return super(SchoolPage,self).save(*args, **kwargs)


class School(models.Model):
    class_name="school"
    title=models.CharField(_("نام مدرسه"), max_length=100)
    

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"school_id": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class Major(SchoolPage):
    courses=models.ManyToManyField("course",blank=True, verbose_name=_("واحد های درسی"))      

    class Meta:
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

    def save(self,*args, **kwargs):
        self.class_name='major'
        return super(Major,self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(models.Model):
    class_name="course"
    title=models.CharField(_("نام واحد درسی "), max_length=100)
    level=models.IntegerField(_("level"))
    books=models.ManyToManyField("book", verbose_name=_("books"),blank=True)
    course_count=models.IntegerField(_("تعداد واحد"))
    def majors(self):
        return self.major_set.all()

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    
    def __str__(self):
        return self.title+" "+str(self.level)+" "

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class EducationalYear(models.Model):
    title=models.CharField(_("title"), max_length=50)
    start_date=models.DateTimeField(_("start_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    
    class_name="educationalyear"
    class Meta:
        verbose_name = _("EducationalYear")
        verbose_name_plural = _("EducationalYears")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class Exam(SchoolPage):
    def save(self,*args, **kwargs):
        if self.class_name is None:
            self.class_name='exam'
        super(Exam,self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")
 
 
class Question(models.Model,LinkHelper):
    exam=models.ForeignKey("exam", verbose_name=_("exam"), on_delete=models.CASCADE)
    question=HTMLField(_("question"), max_length=5000)
    app_name=APP_NAME
    class_name="question"
    def options(self):
        return self.option_set.all().order_by('priority')
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.question
 

class Option(models.Model,LinkHelper):
    question=models.ForeignKey("question", verbose_name=_("question"), on_delete=models.CASCADE)
    priority=models.IntegerField(_("number"))
    option=HTMLField(_("question"), max_length=5000)
    correct=models.BooleanField(_("correct"),default=False)

    app_name=APP_NAME
    class_name="option"

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")
 

    def __str__(self):
        return self.option
 

class ActiveCourse(models.Model):
    class_name="activecourse"
    year=models.ForeignKey("EducationalYear", verbose_name=_("سال تحصیلی"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=200)
    course=models.ForeignKey("course", verbose_name=_("course"), on_delete=models.CASCADE)
    classroom=models.ForeignKey("classroom", verbose_name=_("classroom"), on_delete=models.CASCADE)
    # teacher=models.ForeignKey("teacher", verbose_name=_("teacher"), on_delete=models.CASCADE)
    students=models.ManyToManyField("student", verbose_name=_("students"),blank=True)
    # book=models.ForeignKey("book", verbose_name=_("book"), on_delete=models.CASCADE)

    teachers=models.ManyToManyField("teacher", verbose_name=_("teachers"),blank=True)
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("ActiveCourse")
        verbose_name_plural = _("ActiveCourses")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""


class ClassRoom(models.Model):
    class_name="classroom"
    title=models.CharField(_("نام کلاس"), max_length=100)
    school=models.ForeignKey("school", verbose_name=_("مدرسه"), on_delete=models.CASCADE)
    # courses=models.ManyToManyField("course", verbose_name=_("courses"),blank=True)
    

    

    class Meta:
        verbose_name = _("ClassRoom")
        verbose_name_plural = _("ClassRooms")

    
    def __str__(self):
        return self.school.title+" "+self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class Teacher(models.Model):
    class_name="teacher"
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""


class Session(SchoolPage):
    class_name="session"
    active_course=models.ForeignKey("activecourse", verbose_name=_("activecourse"), on_delete=models.CASCADE)
    session_no=models.IntegerField(_("جلسه شماره ؟"))
    start_time=models.DateTimeField(_("start"), auto_now=False, auto_now_add=False)
    end_time=models.DateTimeField(_("start"), auto_now=False, auto_now_add=False)
    def save(self,*args, **kwargs):
        self.class_name="session"
        return super(Session,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")


    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""


class Attendance(models.Model):
    student=models.ForeignKey("student", verbose_name=_("student"), on_delete=models.CASCADE)
    session=models.ForeignKey("session", verbose_name=_("session"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=AttendanceStatusEnum.choices, max_length=50)
    enter_time=models.DateTimeField(_("enter"),null=True,blank=True, auto_now=False, auto_now_add=False)
    exit_time=models.DateTimeField(_("exit"),null=True,blank=True, auto_now=False, auto_now_add=False)
    time_added=models.DateTimeField(_("time_added"),null=True,blank=True, auto_now=False, auto_now_add=True)
    description=models.CharField(_("description"), max_length=500)
    class_name="attendance"
    def color(self):
        colo="primary"
        if self.status==AttendanceStatusEnum.DELAY:
            colo="warning"
        elif self.status==AttendanceStatusEnum.PRESENT:
            colo="primary"
        elif self.status==AttendanceStatusEnum.ABSENT:
            colo="secondary"
        elif self.status==AttendanceStatusEnum.TASHVIGH:
            colo="success"
        elif self.status==AttendanceStatusEnum.TANBIH:
            colo="danger"
        return colo
    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def __str__(self):
        return self.student.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """

    def persian_enter_time(self):
        return PersianCalendar().from_gregorian(self.enter_time)
    def persian_exit_time(self):
        return PersianCalendar().from_gregorian(self.exit_time)
    def persian_time_added(self):
        return PersianCalendar().from_gregorian(self.time_added)


class Book(LibraryBook): 
    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
 
    def courses(self):
        return self.course_set.all()

    def save(self,*args, **kwargs):
        self.class_name='book'
        self.app_name=APP_NAME
        return super(Book,self).save(*args, **kwargs)


class Student(models.Model):
    class_name="student"
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    
    @property
    def name(self):
        return self.profile.name
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""