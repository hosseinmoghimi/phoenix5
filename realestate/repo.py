from realestate.models import Property
from realestate.apps import APP_NAME
from core.repo import ProfileRepo

class PropertyRepo():
    
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Property.objects
        self.me=ProfileRepo(user=self.user).me
    
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'agent_id' in kwargs:
            objects=objects.filter(agent_id=kwargs['agent_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    
    def property(self,*args, **kwargs):
        if 'property_id' in kwargs:
            pk=kwargs['property_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_property(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_property"):
            return
        property=Property()
        if 'title' in kwargs:
            property.title=kwargs['title']
        if 'area' in kwargs:
            property.area=kwargs['area']
        if 'agent_id' in kwargs:
            property.agent_id=kwargs['agent_id']
        if 'price' in kwargs:
            property.price=kwargs['price']
        if 'address' in kwargs:
            property.address=kwargs['address']
        property.save()
        return property
