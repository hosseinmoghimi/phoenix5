from django.shortcuts import render
from core.views import CoreContext
from django.views import View
from .apps import APP_NAME
from .forms import *
from .repo import ContactRepo
from .serializers import ContactSerializer
import json
from .enums import ContatctNameEnum
from utility.log import leolog


TEMPLATE_ROOT="contact/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)


        contacts=ContactRepo(request=request).list(*args, **kwargs)
        contacts_s=json.dumps(ContactSerializer(contacts,many=True).data)
        context['contacts']=contacts
        context['contacts_s']=contacts_s

        if request.user.has_perm(APP_NAME+".add_contact"):
            context['add_contact_form']=AddContactForm()
            contact_name_enums=list(t[0] for t in ContatctNameEnum.choices)
            context['contact_name_enums']=contact_name_enums
            context['contact_name_enums_s']=json.dumps(contact_name_enums)

        return render(request,TEMPLATE_ROOT+"index.html",context)


class ContactsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if request.user.has_perm(APP_NAME+".add_contact"):
            context['add_contact_form']=AddContactForm()
        return render(request,TEMPLATE_ROOT+"contacts.html",context)