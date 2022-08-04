from core.serializers import ParameterSerializer
import json
from django.http.response import Http404
from core.repo import PageLikeRepo, ParameterRepo, PictureRepo
from django.shortcuts import render,reverse
from core.views import CoreContext, MessageView
from .apps import APP_NAME
from django.views import View
TEMPLATE_ROOT="dashboard/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']="material-dashboard-4/layout.html"
    context['app']={
        'name':APP_NAME,
        'home_url':reverse(APP_NAME+":home"),
    }
    return context
# Create your views here.
class PageLikesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        page_likes=PageLikeRepo(request=request).list(*args, **kwargs)
        context['page_likes']=page_likes
        return render(request,TEMPLATE_ROOT+"page-likes.html",context)
# Create your views here.
class ParameterViews(View):
    
    def get(self,request,*args, **kwargs):
        if not 'app_name' in kwargs:
            
            from log.repo import LogRepo
            LogRepo(request=request).add_log(title="Http404 dashboard views 1",app_name=APP_NAME)
            raise Http404
        if not request.user.has_perm("core.change_parameter"):
            mv=MessageView(request=request,title="دسترسی غیر مجاز",body="<p>شما مجوز لازم برای دسترسی به این صفحه را ندارید.</p>")
            # mv.title="دسترسی غیر مجاز"
            # mv.body="<p>شما مجوز لازم برای دسترسی به این صفحه را ندارید.</p>"
            return mv.response()
        app_name=kwargs['app_name']

        parameters=ParameterRepo(request=request,app_name=app_name).list(*args, **kwargs)
        context=getContext(request=request)
        context['app_name']=app_name
        context['parameters']=parameters
        context['parameters_s']=json.dumps(ParameterSerializer(parameters,many=True).data)
        
        for phoenix_app in context['installed_apps']:
            if phoenix_app['name']==app_name:
                context['selected_app']=phoenix_app

        
        pictures=PictureRepo(request=request,app_name=app_name).list()
        context['pictures']=pictures
        return render(request,TEMPLATE_ROOT+"parameters.html",context)

    def post(self,request,*args, **kwargs):
        pass
class BasicViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"search.html",context)
 