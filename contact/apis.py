from rest_framework.views import APIView
from .forms import *
from .repo import ContactRepo,FAILED,SUCCEED
from .serializers import ContactSerializer
from django.http import JsonResponse

class AddContactApi(APIView):
    def post(self,request,*args, **kwargs):
        message=""
        result=FAILED
        context={}
        if request.method=='POST':
            log=2
            AddContactForm_=AddContactForm(request.POST)
            if AddContactForm_.is_valid():
                cd=AddContactForm_.cleaned_data
                result,message,contacts=ContactRepo(request=request).add_contact(**cd)
                if result==SUCCEED:
                    context['contacts']=ContactSerializer(contacts,many=True).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)
