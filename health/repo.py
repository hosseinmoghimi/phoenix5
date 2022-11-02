from utility.log import leolog
from health.models import Disease, Doctor, Drug, Patient, Visit
from health.apps import APP_NAME
from core.repo import ProfileRepo
from phoenix.constants import FAILED, SUCCEED

class PatientRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Patient.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def patient(self,*args, **kwargs):
        if 'patient_id' in kwargs:
            pk=kwargs['patient_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_patient(self,*args, **kwargs):
        result=FAILED
        patient=None
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_patient"):
            return
        patient=Patient()
        if 'title' in kwargs:
            patient.title=kwargs['title']
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            if len(Patient.objects.filter(account_id=account_id))==0:
                patient.account_id=account_id
                patient.save()
                result=SUCCEED
                message="با موفقیت اضافه شد."
            else:
                message="حساب انتخاب شده تکراری می باشد."

        return patient,result,message

class DoctorRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Doctor.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def doctor(self,*args, **kwargs):
        if 'doctor_id' in kwargs:
            pk=kwargs['doctor_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_doctor(self,*args, **kwargs):
        result=FAILED
        doctor=None
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_doctor"):
            return
        doctor=Doctor()
        if 'title' in kwargs:
            doctor.title=kwargs['title']
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            if len(Doctor.objects.filter(account_id=account_id))==0:
                doctor.account_id=account_id
                doctor.save()
                result=SUCCEED
                message="با موفقیت اضافه شد."
            else:
                message="حساب انتخاب شده تکراری می باشد."

        return doctor,result,message

class DrugRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Drug.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def drug(self,*args, **kwargs):
        if 'drug_id' in kwargs:
            pk=kwargs['drug_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_drug(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_drug"):
            return
        drug=Drug(*args, **kwargs) 
        drug.save()
        return drug

class DiseaseRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Disease.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def disease(self,*args, **kwargs):
        if 'disease' in kwargs:
            return kwargs['disease']
        if 'disease_id' in kwargs:
            pk=kwargs['disease_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_disease(self,*args, **kwargs):
        leolog(add_disease_kwargs=kwargs)
        disease=None
        result=FAILED
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_disease"):
            return
        old_diseases=Disease.objects.filter(name=kwargs['name'])
        if len(old_diseases)>0:
            message="نام تکراری وارد کرده اید."
            return disease,result,message
        disease=Disease(*args, **kwargs) 
        disease.save()
        result=SUCCEED
        message="با موفقیت اضافه شد."
        return disease,result,message

class VisitRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Visit.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'school_id' in kwargs:
            objects=objects.filter(school_id=kwargs['school_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def visit(self,*args, **kwargs):
        if 'visit' in kwargs:
            return kwargs['visit']
        if 'visit_id' in kwargs:
            pk=kwargs['visit_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_visit(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_visit"):
            return
        drug=Drug(*args, **kwargs) 
        drug.save()
        return drug



