from unicodedata import category
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import FAILED,SUCCEED
from market.serializers import CategorySerializerForApi,ProductSerializerForApi
from market.repo import CategoryRepo

class CategoryApi(APIView):
    def get(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        categories=CategoryRepo(request=request).list(*args, **kwargs)
        categories=CategorySerializerForApi(categories,many=True).data
        context['categories']=categories
        context['result']=SUCCEED
        return JsonResponse(context)
class ProductsApi(APIView):
    def get(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        category=CategoryRepo(request=request).category(*args, **kwargs)
        products=category.products.all()
        products=ProductSerializerForApi(products,many=True).data
        context['products']=products
        category=CategorySerializerForApi(category).data
        context['category']=category
        context['result']=SUCCEED
        return JsonResponse(context)
