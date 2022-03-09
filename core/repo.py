from email.policy import default
from .models import Parameter,Picture
from .constants import *
from django.db.models import Q
from authentication.repo import ProfileRepo
from .apps import APP_NAME

class PageRepo:
    pass

class PictureRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Picture.objects.filter(app_name=self.app_name)
    def list(self,*args, **kwargs):
        return self.objects.filter(app_name=self.app_name)
    def picture(self,*args, **kwargs):
        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            if name=="":
                return
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None:
                picture=Picture(app_name=self.app_name,name=name)
                picture.save()
                return picture
            # (picture,res) = self.objects.get_or_create(name=name,app_name=self.app_name)
            # picture = self.objects.filter(name=name).filter(app_name=self.app_name).first()
            return picture
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(pk=pk).first()
        return picture

    def get(self,*args, **kwargs):
        return self.picture(*args, **kwargs)




class ParameterRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=Parameter.objects.filter(app_name=self.app_name)
        if 'force' in kwargs and kwargs['force']:
            self.objects=Parameter.objects.all()
    
    def change_parameter(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+'.change_parameter'):
            return None
        parameter_id=kwargs['parameter_id'] if 'parameter_id' in kwargs else None
        parameter_name=kwargs['parameter_name'] if 'parameter_name' in kwargs else None
        parameter_value=kwargs['parameter_value'] if 'parameter_value' in kwargs else None
        app_name=self.app_name
        if parameter_id is not None:
            parameter=Parameter.objects.filter(pk=parameter_id).first()
            if parameter is None:
                return None
        elif parameter_name is not None and app_name is not None:
            parameter=Parameter.objects.filter(app_name=app_name).filter(name=parameter_name).first()
            if parameter is None:
                parameter=Parameter(app_name=app_name,name=parameter_name,value_origin="")
                parameter.save()
        
        parameter.origin_value=parameter_value
        parameter.save()
        return parameter

    
    def set(self,*args, **kwargs):
        # if name==ParametersEnum.LOCATION:
        #     value=value.replace('width="600"','width="100%"')
        #     value=value.replace('height="450"','height="400"') 
        value=kwargs['value']
        name=kwargs['name']
        if value is None:
            value=name
        parameter=self.parameter(*args, **kwargs)
        parameter.origin_value=value
        parameter.save()
        return parameter
     
    
    
    def parameter(self,*args, **kwargs):
        parameter=None
        parameter_name=""
        if 'parameter_name' in kwargs:
            parameter_name=kwargs['parameter_name']
        if 'name' in kwargs:
            parameter_name=kwargs['name']
        parameter= self.objects.filter(name=parameter_name).first()
        if parameter is None:
            default=parameter_name
            if 'default' in kwargs:
                default=kwargs['default']


            parameter=Parameter(name=parameter_name,app_name=self.app_name,origin_value=default)
            parameter.save()

        if 'id' in kwargs:
            parameter= self.objects.filter(name=kwargs['id']).first()
        if 'parameter_id' in kwargs:
            parameter= self.objects.filter(name=kwargs['parameter_id']).first()
        if 'pk' in kwargs:
            parameter= self.objects.filter(name=kwargs['pk']).first()
            
        return parameter

        

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        return objects

