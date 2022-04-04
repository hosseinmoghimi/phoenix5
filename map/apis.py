from rest_framework.views import APIView

from core.constants import FAILED, SUCCEED
from map.serializers import *
from map.forms import *
from map.repo import AreaRepo, LocationRepo, PageLocationRepo
import json
from django.http import JsonResponse


class AddLocationApi(APIView):
    def post(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_location_form=AddLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location=add_location_form.cleaned_data['location']
                title=add_location_form.cleaned_data['title']
                page_id=add_location_form.cleaned_data['page_id']
                location=LocationRepo(request=request).add_location(location=location,title=title,page_id=page_id)
                
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    

class AddAreaApi(APIView):
    def post(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_area_form=AddAreaForm(request.POST)
            if add_area_form.is_valid():
                log=3
                
                title=add_area_form.cleaned_data['title']
                code=add_area_form.cleaned_data['code']
                area=add_area_form.cleaned_data['area']
                color=add_area_form.cleaned_data['color']
              
                area=AreaRepo(request=request).add_area(
                    title=title,
                    code=code,
                    color=color,
                    area=area,
                )
                
                if area is not None:
                    log=4
                    context['area']=AreaSerializer(area).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    
class AddPageLocationApi(APIView):
    def post(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_location_form=AddPageLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location_id=add_location_form.cleaned_data['location_id']
                page_id=add_location_form.cleaned_data['page_id']
                page_location=PageLocationRepo(request=request).add_page_location(location_id=location_id,page_id=page_id)
                if page_location is not None:
                    log=4
                    page_location_s=PageLocationSerializer(page_location).data
                    return JsonResponse({'result':SUCCEED,'page_location':page_location_s})
        return JsonResponse({'result':FAILED,'log':log})
    