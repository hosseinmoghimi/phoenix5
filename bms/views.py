import json
from django.shortcuts import render
from bms.apps import APP_NAME
from bms.repo import FeederRepo
from core.views import CoreContext
from bms.serializers import FeederFullSerializer, FeederSerializer, RelaySerializer
from django.views import View

TEMPLATE_ROOT="bms/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)

        return render(request,TEMPLATE_ROOT+"index.html",context)
class FeedersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeders=FeederRepo(request=request).list()
        context['feeders']=feeders
        feeders_s=json.dumps(FeederSerializer(feeders,many=True).data)
        context['feeders_s']=feeders_s
        return render(request,TEMPLATE_ROOT+"feeders.html",context)


        
class FeederView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feeder=FeederRepo(request=request).feeder(*args, **kwargs)
        context['feeder']=feeder
        feeder_s=json.dumps(FeederFullSerializer(feeder).data)
        context['feeder_s']=feeder_s

        
        # relays=feeder.relay_set.all()
        # context['relays']=relays
        # relays_s=json.dumps(RelaySerializer(relays,many=True).data)
        # context['relays_s']=relays_s

        return render(request,TEMPLATE_ROOT+"feeder.html",context)