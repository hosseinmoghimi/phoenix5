import requests
from bms.models import Feeder, Log,Relay,Command
from authentication.repo import ProfileRepo
from bms.apps import APP_NAME
from utility.log import leolog
from core.constants import SUCCEED,FAILED


class FeederRepo():
     
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = Feeder.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects.all()

    def feeder(self, *args, **kwargs):
        if 'feeder_id' in kwargs:
            return self.objects.filter(pk=kwargs['feeder_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location1=""
        title=""
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            title=kwargs['title']
        location=Location()
        location.title=title
        location.creator=self.profile
        location.location=location1
        location.latitude="gfgf"
        location.longitude="gfgf"
        location.save()
        if 'page_id' in kwargs and kwargs['page_id'] is not None and kwargs['page_id']>0:
            page_location=PageLocation()
            page_location.page_id=kwargs['page_id']
            page_location.location=location
            page_location.save()
        return location
     
class LogRepo():
     
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = Log.objects

    def list(self,*args, **kwargs):
        objects= self.objects
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects.all()

    def log(self, *args, **kwargs):
        if 'log_id' in kwargs:
            return self.objects.filter(pk=kwargs['log_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            

      
class CommandRepo():
     
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = Command.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects.all()

    def command(self, *args, **kwargs):
        if 'command' in kwargs:
            return kwargs['command']
        if 'command_id' in kwargs:
            return self.objects.filter(pk=kwargs['command_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            
 
    def execute_command(self,*args, **kwargs):
        leolog(kwargs=kwargs)
        result=FAILED
        message=""
        registers=[]

        command=self.command(*args, **kwargs)
        if command is not None:
            if not self.profile in command.profiles.all():
                return FAILED,None,message
           
            if self.profile in command.profiles.all():
                ip=command.relay.feeder.ip
                relay_pin= kwargs['pin'] if (command.relay.is_protected and 'pin' in kwargs) else command.relay.pin
                if relay_pin==command.relay.pin:
                    leolog(relay_pin=relay_pin)
                    port=command.relay.feeder.port
                    register=command.relay.register
                    command_value=command.value
                    payload={'register':register,'command':command_value,'key':relay_pin,'pin':relay_pin}
                    leolog(payload=payload)
                    from .client import handleExecuteCommand_url
                    url=f'http://{ip}:{port}/'+handleExecuteCommand_url
                    try:
                        response=requests.post(url,payload)
                    except:
                        Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=False).save()
                        return FAILED,None,message
                    registers=response.json()['registers']
                    relays=command.relay.feeder.relay_set.all()
                    for register in registers:
                        register_no=int(register['register'])
                        if register is not None:
                            relay=relays.get(register=register_no)
                            if register_no==command.relay.register:
                                pass
                            state=int(register['state'])==1
                            relay.current_state=state
                            relay.save()
                    Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=True).save()
                    return SUCCEED,registers,message
            Log(title=command.name,feeder=command.relay.feeder,relay=command.relay,profile=self.profile,command=command,succeed=False).save()
        return FAILED,None,message
