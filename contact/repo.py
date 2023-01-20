from .models import Contact
from authentication.repo import ProfileRepo
from .apps import APP_NAME
from django.db.models import Q
from core.constants import FAILED,SUCCEED
from .enums import ContatctNameEnum

class ContactRepo():
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
        self.objects=Contact.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            return objects.filter(Q(name__contains=kwargs['search_for'])|Q(value__contains=kwargs['search_for'])|Q(account__title__contains=kwargs['search_for']))
        return objects.all()
    def contact(self,*args, **kwargs):
        if 'contact_id' in kwargs:
            return self.objects.filter(pk=kwargs['contact_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    
    def add_contact(self,*args, **kwargs):
        result,message,contacts=FAILED,"",[]
        if not self.request.user.has_perm(APP_NAME+".add_contact"):
            return result,message,contacts
        contact=Contact()
        if 'name' in kwargs:
            contact.name=kwargs['name']
        if 'value' in kwargs:
            contact.value=kwargs['value']
        if 'url' in kwargs:
            contact.url=kwargs['url']
        if 'account_id' in kwargs:
            contact.account_id=kwargs['account_id']
        if 'account' in kwargs:
            contact.account=kwargs['account'] 
        contact.save()
        if contact.name==ContatctNameEnum.MOBILE:
            Contact(name=ContatctNameEnum.TELEGRAM,value=contact.value,account_id=contact.account_id).save()
            Contact(name=ContatctNameEnum.WHATSAPP,value=contact.value,account_id=contact.account_id).save()
        if contact is not None:
            result=SUCCEED
            message="با موفقیت اضافه شد."
        contacts=Contact.objects.filter(accout_id=contact.account_id)
        return result,message,contacts

