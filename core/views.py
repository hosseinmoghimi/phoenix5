from django.shortcuts import render
from core.enums import ParameterNameEnum
from core.repo import ParameterRepo
from phoenix.settings import ADMIN_URL,MEDIA_URL,STATIC_URL
from django.shortcuts import render
from authentication.repo import ProfileRepo
from core.constants import CURRENCY
from django.views import View
from .forms import *
# Create your views here.
def CoreContext(request,app_name,*args, **kwargs):
    context={}
    context['APP_NAME']=app_name
    context['ADMIN_URL']=ADMIN_URL
    context['STATIC_URL']=STATIC_URL
    context['MEDIA_URL']=MEDIA_URL
    context['profile']=ProfileRepo(request=request).me
    parameter_repo = ParameterRepo(request=request,app_name=app_name)
    # (parameter,res)=ParameterRepo(request=request,app_name='core').objects.get_or_create(name=ParameterNameEnum.CURRENCY)
    # context['CURRENCY']=parameter.value
    context['CURRENCY']=CURRENCY
    farsi_font_name=parameter_repo.parameter(name=ParameterNameEnum.FARSI_FONT_NAME).value
    if not farsi_font_name==ParameterNameEnum.FARSI_FONT_NAME and not farsi_font_name=="Default":
        context['farsi_font_name']=farsi_font_name
    
    context['app']={
        'title':parameter_repo.parameter(name=ParameterNameEnum.TITLE).value,
        'home_url':parameter_repo.parameter(name=ParameterNameEnum.HOME_URL).value,
    }
    return context

class MessageView():
    pass