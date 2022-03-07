from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View
from .apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json


TEMPLATE_ROOT = "projectmanager/"
LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
