from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse,Http404
from accounting.serializers import CategorySerializer,ProductBriefSerializer
from accounting.repo import CategoryRepo,ProductRepo
# Create your views here.
class Categories(APIView):
    def get(self,request,*args, **kwargs):
        context={}
        categories=CategoryRepo(request=request).list()
        categories_s=CategorySerializer(categories,many=True).data
        context["categories"]=categories_s
        return JsonResponse(context)
class Products(APIView):
    def get(self,request,*args, **kwargs):
        category=CategoryRepo(request=request).category(*args, **kwargs)
        context={}
        if category is not None:
            products=ProductRepo(request=request).list(category_id=category.id)
        else:
            products=[]
        products_s=ProductBriefSerializer(products,many=True).data
        context["products"]=products_s
        return JsonResponse(context)