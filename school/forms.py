from django import forms

from .apps import APP_NAME

class SearchForm(forms.Form):
    
    url=("/"+APP_NAME+"/search/")
    search_for=forms.CharField( max_length=50, required=True)


class AddEducationalYearForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
    start_date=forms.CharField( max_length=50, required=True)
    end_date=forms.CharField( max_length=50, required=True)


class AddSchoolForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
    account_id=forms.IntegerField(required=True)

class AddClassRoomForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)
    school_id=forms.IntegerField(required=True)


class AddQuestionForm(forms.Form):
    exam_id=forms.IntegerField(required=True)
    question=forms.CharField( max_length=50, required=True)

class SelectOptionForm(forms.Form):
    option_id=forms.IntegerField(required=True)


class AddExamForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)


class AddMajorForm(forms.Form):
    title=forms.CharField( max_length=50, required=True)


class AddTeacherForm(forms.Form):
    account_id=forms.IntegerField( required=True)


class AddStudentForm(forms.Form):
    account_id=forms.IntegerField( required=True)


class AddSessionForm(forms.Form):
    active_course_id=forms.IntegerField( required=True)


class AddAttendanceForm(forms.Form):
    student_id=forms.IntegerField( required=True)
    session_id=forms.IntegerField( required=True)
    status=forms.CharField( max_length=50, required=True)
    description=forms.CharField( max_length=500, required=False)
    time=forms.CharField( max_length=50, required=False)


class AddDocumentForm(forms.Form):
    book_id=forms.IntegerField( required=True)
    title=forms.CharField( max_length=50, required=True)


class AddBookForm(forms.Form):
    course_id=forms.IntegerField( required=True)
    title=forms.CharField( max_length=50, required=True)


class AddActiveCourseForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    course_id=forms.IntegerField( required=True)
    classroom_id=forms.IntegerField(required=True)


class AddCourseForm(forms.Form):
    course_count=forms.IntegerField( required=True)
    level=forms.IntegerField( required=True)
    major_id=forms.IntegerField( required=True)
    title=forms.CharField( max_length=50, required=True)

class AddBookToCourseForm(forms.Form):
    book_id=forms.IntegerField( required=True)
    course_id=forms.IntegerField( required=True)


class AddStudentToActiveCourseForm(forms.Form):
    student_id=forms.IntegerField( required=True)
    # profile_id=forms.IntegerField( required=True)
    active_course_id=forms.IntegerField( required=True)


class AddTeacherToActiveCourseForm(forms.Form):
    teacher_id=forms.IntegerField( required=True)
    # profile_id=forms.IntegerField( required=True)
    active_course_id=forms.IntegerField( required=True)