from django.http.response import JsonResponse
from django.utils import timezone
from core.serializers import DownloadSerializer
from school.forms import *
from school.repo import ActiveCourseRepo, AttendanceRepo, BookRepo, ClassRoomRepo, CourseRepo, EducationalYearRepo, ExamRepo, MajorRepo, SchoolRepo, SessionRepo, StudentRepo, TeacherRepo
from school.serializers import ActiveCourseSerializer, AttendanceSerializer, BookSerializer, ClassRoomSerializer, CourseSerializer, EducationalYearSerializer, ExamSerializer, MajorSerializer, OptionFullSerializer, OptionSerializer, QuestionSerializer, SchoolSerializer, SessionSerializer, StudentSerializer, TeacherSerializer
from utility.calendar import PersianCalendar
from .apps import APP_NAME
from rest_framework.views import APIView
from utility.log import leolog
from core.constants import SUCCEED,FAILED
class AddEducationalYearApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        message=""
        add_educational_year=AddEducationalYearForm(request.POST)
        if add_educational_year.is_valid():
            cd=add_educational_year.cleaned_data
            cd['start_date']=PersianCalendar().to_gregorian(cd['start_date'])
            cd['end_date']=PersianCalendar().to_gregorian(cd['end_date'])
            educational_year,message,result=EducationalYearRepo(request=request).add(**cd)
            if result==SUCCEED:
                context['result']=result
                context['educational_year']=EducationalYearSerializer(educational_year).data
        context['message']=message
        return JsonResponse(context)


class SchoolApi(APIView):
    def add_school(self,request,*args, **kwargs):
        context={'result':FAILED}
        message=""
        result=FAILED
        log=1
        if request.method=='POST':
            log=2
            my_form=AddSchoolForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                school,result,message=SchoolRepo(request=request).add(**cd)
                if result==SUCCEED:
                    context['school']=SchoolSerializer(school).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)


class CourseApi(APIView):
    def add_course(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddCourseForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                major_id=cd['major_id']
                course_count=cd['course_count']
                level=cd['level']
                course=CourseRepo(request=request).add_course(title=title,major_id=major_id,level=level,course_count=course_count)
                if course is not None:
                    context['course']=CourseSerializer(course).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class AddStudentToActiveCourseApi(APIView):

    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        result=FAILED
        log=2
        my_form=AddStudentToActiveCourseForm(request.POST)
        if my_form.is_valid():
            log=3
            cd=my_form.cleaned_data
            student=ActiveCourseRepo(request=request).add_student_to_active_course(**my_form.cleaned_data)
            if student is not None:
                context['student']=StudentSerializer(student).data
                result=SUCCEED
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
class AddActiveCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        log=2
        my_form=AddActiveCourseForm(request.POST)
        if my_form.is_valid():
            log=3
            cd=my_form.cleaned_data
            title=cd['title']
            classroom_id=cd['classroom_id']
            course_id=cd['course_id']
            active_course=ActiveCourseRepo(request=request).add_active_course(title=title,classroom_id=classroom_id,course_id=course_id)
            if active_course is not None:
                context['active_course']=ActiveCourseSerializer(active_course).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
class AddTeacherToActiveCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        log=2
        my_form=AddTeacherToActiveCourseForm(request.POST)
        if my_form.is_valid():
            log=3
            teacher=ActiveCourseRepo(request=request).add_teacher_to_active_course(**my_form.cleaned_data)
            if teacher is not None:
                context['teacher']=TeacherSerializer(teacher).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    
class AddBookToCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        log=2
        my_form=AddBookToCourseForm(request.POST)
        if my_form.is_valid():
            log=3
            book=CourseRepo(request=request).add_book_to_course(**my_form.cleaned_data)
            if book is not None:
                context['book']=BookSerializer(book).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class AddExamApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1

        add_exam_form=AddExamForm(request.POST)
        if add_exam_form.is_valid():
            log=3
            cd=add_exam_form.cleaned_data
            title=cd['title']
            exam=ExamRepo(request=request).add_exam(title=title)
            if exam is not None:
                context['exam']=ExamSerializer(exam).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
class AddQuestionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1

        add_question_form=AddQuestionForm(request.POST)
        if add_question_form.is_valid():
            log=3
            cd=add_question_form.cleaned_data
            question=cd['question']
            exam_id=cd['exam_id']
            question=ExamRepo(request=request).add_question(question=question,exam_id=exam_id)
            if question is not None:
                context['question']=QuestionSerializer(question).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class SelectOptionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1

        select_option_form=SelectOptionForm(request.POST)
        if select_option_form.is_valid():
            log=3
            cd=select_option_form.cleaned_data
            option_id=cd['option_id']
            option=ExamRepo(request=request).select_option(option_id=option_id)
            if option is not None:
                context['option']=OptionFullSerializer(option).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class BookApi(APIView):
    def add_document(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_document_form=AddDocumentForm(request.POST)
            if add_document_form.is_valid():
                log=3
                cd=add_document_form.cleaned_data
                title=cd['title']
                book_id=cd['book_id']
                document=BookRepo(request=request).add_document(title=title,book_id=book_id)
                if document is not None:
                    context['document']=DocumentSerializer(document).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_book(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            add_book_form=AddBookForm(request.POST)
            if add_book_form.is_valid():
                log=3
                cd=add_book_form.cleaned_data
                title=cd['title']
                course_id=cd['course_id']
                book=BookRepo(request=request).add_book(title=title,course_id=course_id)
                if book is not None:
                    context['book']=BookSerializer(book).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class SessionApi(APIView):
    def add_session(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddSessionForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                active_course_id=cd['active_course_id']
                session=SessionRepo(request=request).add_session(active_course_id=active_course_id)
                if session is not None:
                    context['session']=SessionSerializer(session).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class AttendanceApi(APIView):
    def add_attendance(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddAttendanceForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                description=cd['description']
                student_id=cd['student_id']
                session_id=cd['session_id']
                # time=cd['time']
                # if time=="NOW":
                #     time=PersianCalendar().date
                status=cd['status']
                attendances=AttendanceRepo(request=request).add(
                    student_id=student_id,
                    session_id=session_id,
                    status=status,
                    description=description,
                    )
                if attendances is not None:
                    context['attendances']=AttendanceSerializer(attendances,many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
  
class AddStudentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddStudentForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                result,message,student=StudentRepo(request=request).add_student(**cd)
                if result ==SUCCEED:
                    context['student']=StudentSerializer(student).data
                context['result']=result
                context['message']=message
        context['log']=log
        return JsonResponse(context)


class AddTeacherApi(APIView):
    def post(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddTeacherForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                result,message,teacher=TeacherRepo(request=request).add_teacher(**cd)
                if result ==SUCCEED:
                    context['teacher']=TeacherSerializer(teacher).data
                context['result']=result
                context['message']=message
        context['log']=log
        return JsonResponse(context)



class ClassRoomApi(APIView):
    def add_classroom(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddClassRoomForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                school_id=cd['school_id']
                classroom=ClassRoomRepo(request=request).add(title=title,school_id=school_id)
                if classroom is not None:
                    context['classroom']=ClassRoomSerializer(classroom).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class MajorApi(APIView):
    def add_major(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            my_form=AddMajorForm(request.POST)
            if my_form.is_valid():
                log=3
                cd=my_form.cleaned_data
                title=cd['title']
                major=MajorRepo(request=request).add(title=title)
                if major is not None:
                    context['major']=MajorSerializer(major).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)