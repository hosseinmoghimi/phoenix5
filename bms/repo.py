from bms.models import Feeder,Relay,Command
from authentication.repo import ProfileRepo
from bms.apps import APP_NAME
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
     