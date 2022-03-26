from django.http import Http404, JsonResponse
from django.shortcuts import render,reverse
from core.constants import CURRENCY, FAILED, SUCCEED 
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View

from utility.calendar import PersianCalendar
from .apps import APP_NAME
from .repo import FolderRepo
from .serializers import FolderSerializer
from .forms import *
import json


LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "archive/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        return FolderView().get(request=request,pk=1)





class SearchView(View):
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context['search_for']=search_for
            folders=FolderRepo(request=request).list(search_for=search_for)
            context['folders']=folders
        return render(request,TEMPLATE_ROOT+"folder.html",context)




class FolderView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        folder=FolderRepo(request=request).folder(*args, **kwargs)
        context['folder']=folder
        folders=FolderRepo(request=request).list(parent_id=folder.pk)

        
        context['folders']=folders


        context['open_folder_form']=OpenFolderForm()
        if request.user.has_perm(APP_NAME+".add_folder"):
            context['create_folder_form']=CreateFolderForm()
        return render(request,TEMPLATE_ROOT+"folder.html",context)
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        open_folder_form=OpenFolderForm(request.POST)
        if open_folder_form.is_valid():
            folder_id=open_folder_form.cleaned_data['folder_id']
            folder=FolderRepo(request=request).folder(folder_id=folder_id)
            folders=folder.childs.all()
            context['folder']=FolderSerializer(folder).data
            context['folders']=FolderSerializer(folders,many=True).data
            context['result']=SUCCEED
        return JsonResponse(context)

 
class CreateFolderApi(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        create_folder_form=CreateFolderForm(request.POST)
        if create_folder_form.is_valid():
            folder=FolderRepo(request=request).create_folder(**create_folder_form.cleaned_data)
            context['folder']=FolderSerializer(folder).data
            context['result']=SUCCEED
        return JsonResponse(context)

 