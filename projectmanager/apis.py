import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import PageLinkSerializer
from .enums import *

from utility.calendar import PersianCalendar
from .repo import  OrganizationUnitRepo
from django.http import JsonResponse
from .forms import *
from .serializers import OrganizationUnitSerializer

class AddOrganizationUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            AddOrganizationUnitForm_=AddOrganizationUnitForm(request.POST)
            if AddOrganizationUnitForm_.is_valid():
                log=3
                fm=AddOrganizationUnitForm_.cleaned_data
                title=fm['title']
                parent_id=fm['parent_id']
                page_id=fm['page_id']
                organization_unit_id=fm['organization_unit_id']
                organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(
                    title=title,
                    parent_id=parent_id,
                    organization_unit_id=organization_unit_id,
                    page_id=page_id,
                )
                if organization_unit is not None:
                    context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)