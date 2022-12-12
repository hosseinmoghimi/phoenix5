from unittest import result
from urllib import request
from authentication.repo import ProfileRepo
from phoenix.constants import FAILED, SUCCEED
from library.repo import BookRepo
from school.enums import AttendanceStatusEnum
from school.forms import SelectOptionForm
from utility.log import leolog
from .models import ActiveCourse, Attendance, ClassRoom, Course, EducationalYear, Exam, Major, Question, School, SelectedOption, Session,Student,Teacher,Book
from .apps import APP_NAME
from django.db.models import Q
from django.utils import timezone
from utility.calendar import PersianCalendar
from accounting.models import Transaction

class AttendanceRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Attendance.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'session_id' in kwargs:
            objects=objects.filter(session_id=kwargs['session_id'])
        if 'student_id' in kwargs:
            objects=objects.filter(student_id=kwargs['student_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def attendance(self,*args, **kwargs):
        if 'attendance_id' in kwargs:
            return self.objects.filter(pk=kwargs['attendance_id']).first()
        elif 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        elif 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    def add(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_attendance"):
            return
        now=PersianCalendar().date
        session_id=kwargs['session_id'] if 'session_id' in kwargs else 0
        student_id=kwargs['student_id'] if 'student_id' in kwargs else 0
        description=kwargs['description'] if 'description' in kwargs else 0
        status=kwargs['status'] if 'status' in kwargs else AttendanceStatusEnum.NOT_SET

        session=SessionRepo(request=self.request).session(pk=session_id)
        student=StudentRepo(request=self.request).student(pk=student_id)

        if session is None or student is None:
            return
        enter_time=kwargs['enter_time'] if 'enter_time' in kwargs else session.start_time
        exit_time=kwargs['exit_time'] if 'exit_time' in kwargs else session.end_time
        if status==AttendanceStatusEnum.ABSENT:
            Attendance.objects.filter(student_id=student.id).filter(session_id=session.id).delete()
        if status==AttendanceStatusEnum.PRESENT:
            Attendance.objects.filter(student_id=student.id).filter(session_id=session.id).filter(Q(status=AttendanceStatusEnum.PRESENT)|Q(status=AttendanceStatusEnum.ABSENT)|Q(status=AttendanceStatusEnum.DELAY)).delete()
        if status==AttendanceStatusEnum.DELAY:
            Attendance.objects.filter(student_id=student.id).filter(session_id=session.id).filter(Q(status=AttendanceStatusEnum.PRESENT)|Q(status=AttendanceStatusEnum.ABSENT)|Q(status=AttendanceStatusEnum.DELAY)).delete()
        attendance=Attendance()
        attendance.student=student
        attendance.session=session
        attendance.enter_time=enter_time
        attendance.exit_time=exit_time
        attendance.status=status
        attendance.description=description
        attendance.save()
        attendances=Attendance.objects.filter(session_id=session.id).order_by('-time_added')
        return attendances
class SchoolRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = School.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def school(self,*args, **kwargs):
        if 'school_id' in kwargs:
            pk=kwargs['school_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        school=None
        result=FAILED
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_school"):
            message="عدم دسترسی"
            return school,result,message
        school=School()
        if len(School.objects.filter(title=kwargs['title']))>0:
            message="نام آموزشگاه تکراری می باشد"
            return school,result,message
        if 'title' in kwargs:
            school.title=kwargs['title']
        if 'account_id' in kwargs:
            school.account_id=kwargs['account_id']
        school.save()
        if school is not None:
            result=SUCCEED
            message="آموزشگاه جدید با موفقیت اضافه شد."
        return school,result,message

class MajorRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Major.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def major(self,*args, **kwargs):
        if 'major_id' in kwargs:
            pk=kwargs['major_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_major"):
            return
        major=Major()
        if 'title' in kwargs:
            major.title=kwargs['title']
        major.save()
        return major
    
class ExamRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Exam.objects
        self.profile=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'course_id' in kwargs:
            course=CourseRepo(request=self.request).course(pk=kwargs['course_id'])
            if course is not None:
                return course.books.all()
            return
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def exam(self,*args, **kwargs):
        if 'exam_id' in kwargs:
            pk=kwargs['exam_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_exam(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_exam"):
            return
        exam=Exam(*args, **kwargs)
        exam.save() 
        return exam
 

    def add_question(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_question"):
            return
        question=Question(*args, **kwargs)
        question.save() 
        return question
 
    def select_option(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_selectedoption"):
            return
        select_option=SelectedOption(*args, **kwargs)
        select_option.student=StudentRepo(request=self.request).me
        select_option.save() 
        return select_option.option

class BookRepo2():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Book.objects
        self.profile=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'course_id' in kwargs:
            course=CourseRepo(request=self.request).course(pk=kwargs['course_id'])
            if course is not None:
                return course.books.all()
            return
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def book(self,*args, **kwargs):
        if 'book_id' in kwargs:
            pk=kwargs['book_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_document(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_book"):
            return
        document=Document()
        if 'title' in kwargs:
            document.title=kwargs['title']
        document.icon_fa='fa fa-download'
        document.profile_id=self.profile.id
        document.save()
        book=self.book(*args, **kwargs)
        if book is None:
            return
        book.documents.add(document)
        return document

    def add_book(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_book"):
            return
        book=Book()
        if 'title' in kwargs:
            book.title=kwargs['title']
        book.save()
        course=CourseRepo(request=self.request).course(*args, **kwargs)
        if course is None:
            return
        course.books.add(book)
        return book


class ClassRoomRepo():
   
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ClassRoom.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def classroom(self,*args, **kwargs):
        if 'classroom_id' in kwargs:
            pk=kwargs['classroom_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_classroom"):
            return
        classroom=ClassRoom()
        if 'title' in kwargs:
            classroom.title=kwargs['title']
        if 'school_id' in kwargs:
            classroom.school_id=kwargs['school_id']
        classroom.save()
        return classroom

class ActiveCourseRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ActiveCourse.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(classroom__school_id=kwargs['school_id'])
        if 'class_room_id' in kwargs:
            objects=objects.filter(classroom_id=kwargs['class_room_id'])
        if 'year_id' in kwargs:
            objects=objects.filter(year_id=kwargs['year_id'])
        return objects
    
    def active_course(self,*args, **kwargs):
        if 'active_course_id' in kwargs:
            pk=kwargs['active_course_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_active_course(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_activecourse"):
            return
            active_course.end_date=kwargs['start_date']
        now=PersianCalendar().date
        active_course=ActiveCourse()
        if 'title' in kwargs:
            active_course.title=kwargs['title']
        if 'classroom_id' in kwargs:
            active_course.classroom_id=kwargs['classroom_id']
        if 'course_id' in kwargs:
            active_course.course_id=kwargs['course_id']
        if 'start_date' in kwargs:
            active_course.start_date=kwargs['start_date']
        else:
            active_course.start_date=now
        if 'end_date' in kwargs:
            active_course.end_date=kwargs['end_date']
        else:
            active_course.end_date=now

            
        if 'year_id' in kwargs:
            active_course.year_id=kwargs['year_id']
        else:
            year_id=EducationalYear.objects.last().id
            active_course.year_id=year_id
        active_course.save()
        return active_course
        

    def add_teacher_to_active_course(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_activecourse"):
            return
        active_course=self.active_course(*args, **kwargs)
        teacher=Teacher.objects.filter(pk=kwargs['teacher_id']).first()
        if teacher is None:
            result=FAILED
            return

        if active_course is None or teacher is None:
            return
        if not teacher in active_course.teachers.all():

            active_course.teachers.add(teacher)
            return teacher
        
        
    def add_student_to_active_course(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_activecourse"):
            return
        active_course=self.active_course(*args, **kwargs)
        student=Student.objects.filter(pk=kwargs['student_id']).first()
        if student is None:
            result=FAILED
            return

        if active_course is None or student is None:
            return
        if not student in active_course.students.all():
            active_course.students.add(student)
            if active_course.cost>0:
                transaction=Transaction()
                transaction.pay_to=student.account
                transaction.pay_from=active_course.class_room.school.account
                transaction.save()
            return student



class CourseRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Course.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    def course(self,*args, **kwargs):
        if 'course_id' in kwargs:
            pk=kwargs['course_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_book_to_course(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_activecourse"):
            return
        course=self.course(*args, **kwargs)
        book=BookRepo(request=self.request).book(*args, **kwargs)
       

        if course is None or book is None:
            result=FAILED
            return
        if not book in course.books.all():
            course.books.add(book)
            return book

    def add_course(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_course"):
            return
        course=Course()
        if 'title' in kwargs:
            course.title=kwargs['title']
        if 'level' in kwargs:
            course.level=kwargs['level']
        if 'course_count' in kwargs:
            course.course_count=kwargs['course_count']
        course.save()
        if 'major_id' in kwargs:
            major=MajorRepo(request=self.request).major(pk=kwargs['major_id'])
            if major is not None:
                major.courses.add(course)
        return course
        

class SessionRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Session.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
    def session(self,*args, **kwargs):
        if 'session_id' in kwargs:
            pk=kwargs['session_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_session(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_session"):
            return
        session=Session()
        if 'active_course_id' in kwargs:

            active_course_id=kwargs['active_course_id']
        else:
            return
        active_course=ActiveCourse.objects.filter(pk=active_course_id).first()
        if active_course is None:
            return

        session_no=1
        session.active_course_id=active_course_id
        if 'session_no' in kwargs:
            session_no=kwargs['session_no']
        else:
            session_1=Session.objects.filter(active_course_id=active_course_id).order_by('-session_no').first()
            if session_1 is not None:
                session_no=1+session_1.session_no

        session.session_no=session_no
        if 'title' in kwargs:
            session.title=kwargs['title']
        else:
            session.title="جلسه "+str(session_no)+" "+active_course.course.title
        
        if 'start_time' in kwargs:
            session.start_time=kwargs['start_time']
        else:
            session.start_time=PersianCalendar().date
        
        if 'end_time' in kwargs:
            session.end_time=kwargs['end_time']
        else:
            session.end_time=PersianCalendar().date

        session.save()
        return session

  

    
class TeacherRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Teacher.objects
        self.profile=ProfileRepo(user=self.user).me
        self.me=Teacher.objects.filter(account__profile=self.profile).first()
        if self.request.user.has_perm(APP_NAME+".view_teacher"):
            self.objects = Teacher.objects
        elif self.me is not None:
            self.objects = Teacher.objects.filter(pk=self.me.pk)
        else:
            self.objects=Teacher.objects.filter(pk=0)
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(profile__user__first_name__contains=kwargs['search_for'])|Q(profile__user__last_name__contains=kwargs['search_for']))
        return objects
    def teacher(self,*args, **kwargs):
        if 'profile_id' in kwargs:
            return self.objects.filter(profile_id=kwargs['profile_id']).first()
        if 'teacher_id' in kwargs:
            return self.objects.filter(pk=kwargs['teacher_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
         
 

    def add_teacher(self,*args, **kwargs):
        result=FAILED
        message=""
        teacher=None
        if not self.request.user.has_perm(APP_NAME+".add_teacher"):
            return
        account_id=kwargs['account_id']
        teacher=Teacher.objects.filter(account_id=account_id).first()
        if teacher is not None:
            result=FAILED
            message="قبلا دبیری با این اکانت ایجاد شده است."
            return result,message,teacher
        teacher=self.teacher(*args, **kwargs)
        if teacher is None:
            teacher=Teacher()
            teacher.account_id=account_id
            teacher.save()
        if teacher is not None:
            result=SUCCEED
            message="دبیر جدید با موفقیت افزوده شد."
        return result,message,teacher

    

    
class StudentRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.me=Student.objects.filter(account__profile=self.profile).first()
        if self.request.user.has_perm(APP_NAME+".view_student"):
            self.objects = Student.objects
        elif self.me is not None:
            self.objects = Student.objects.filter(pk=self.me.pk)
        else:
            self.objects=Student.objects.filter(pk=0)

    def list(self,*args, **kwargs):
        
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(profile__user__first_name__contains=kwargs['search_for'])|Q(profile__user__last_name__contains=kwargs['search_for']))
        return objects
    def student(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            return self.objects.filter(profile_id=kwargs['profile_id']).first()
        if 'student_id' in kwargs:
            pk=kwargs['student_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    

    def add_student(self,*args, **kwargs):
        result=FAILED
        message=""
        student=None
        if not self.request.user.has_perm(APP_NAME+".add_student"):
            return
        account_id=kwargs['account_id']
        student=Student.objects.filter(account_id=account_id).first()
        if student is not None:
            result=FAILED
            message="قبلا دانش آموزی با این اکانت ایجاد شده است."
            return result,message,student
        student=self.student(*args, **kwargs)
        if student is None:
            student=Student()
            student.account_id=account_id
            student.save()
        if student is not None:
            result=SUCCEED
            message="دانش آموز جدید با موفقیت افزوده شد."
        return result,message,student

    
class EducationalYearRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = EducationalYear.objects
        self.profile=ProfileRepo(user=self.user).me
        self.me=Student.objects.filter(account__profile=self.profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(profile__user__first_name__contains=kwargs['search_for'])|Q(profile__user__last_name__contains=kwargs['search_for']))
        return objects
    def add(self,*args, **kwargs):
        result=FAILED
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_educationalyear"):
            return
        educational_year=EducationalYear(*args, **kwargs)
        if educational_year.start_date>=educational_year.end_date:
            message="تاریخ شروع و پایان صحیح نیست"
            educational_year=None
            result=FAILED
            return educational_year,message,result

        
        if len(EducationalYear.objects.filter(title=educational_year.title))>0:
            message="عنوان سال تحصیلی تکراری می باشد."
            educational_year=None
            result=FAILED
            return educational_year,message,result

        
        educational_year.save()
        if educational_year is not None:
            result=SUCCEED
            message="سال تحصیلی جدید با موفقیت افزوده شد."

        return educational_year,message,result
    def educational_year(self,*args, **kwargs):
        if 'educational_year_id' in kwargs:
            return self.objects.filter(pk=kwargs['educational_year_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    
