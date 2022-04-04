from django.shortcuts import render,reverse
import json
from core.enums import ColorEnum, ParameterNameEnum

from core.repo import ParameterRepo
from map.forms import AddAreaForm, AddLocationForm
from .repo import *
from .serializers import *
from django.http import Http404
from django.views import View
from core.views import CoreContext, MessageView
from .apps import APP_NAME
TEMPLATE_ROOT = APP_NAME+"/"
LAYOUT_PARENT = "phoenix/layout.html"


def getContext(request):
    user = request.user
    context = CoreContext(request=request, app_name=APP_NAME)
    # parameter_repo = ParameterRepo(app_name=APP_NAME)
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context

 
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        return render(request, TEMPLATE_ROOT+"index.html", context)


class LocationView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        location = LocationRepo(request=request).location(*args, **kwargs)
        context['location'] = location
        context['location_s'] = json.dumps(LocationSerializer(location).data)

        return render(request, TEMPLATE_ROOT+"location.html", context)
  

class AreaView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        area = AreaRepo(request=request).area(*args, **kwargs)
        context['area'] = area
        context['area_s'] = json.dumps(AreaSerializer(area).data)
        return render(request, TEMPLATE_ROOT+"area.html", context)


class AreasView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        areas = AreaRepo(request=request).list(*args, **kwargs)
        context['areas'] = areas
        context['areas_s'] = json.dumps(AreaSerializer(areas,many=True).data)
        if request.user.has_perm(APP_NAME+".add_area"):
            context['add_area_form']=AddAreaForm()
            context['colors']=(color[0] for color in ColorEnum.choices)
        return render(request, TEMPLATE_ROOT+"areas.html", context)


class LocationsView(View):  
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        locations = LocationRepo(request=request).list(*args, **kwargs)
        context['locations'] = locations
        context['locations_s'] = json.dumps(LocationSerializer(locations,many=True).data)
        if request.user.has_perm(APP_NAME+".add_location"):
            context['add_location_form']=AddLocationForm()
        return render(request, TEMPLATE_ROOT+"locations.html", context)