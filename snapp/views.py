from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext
import json
from .serializers import CategorySerializer,ProductSerializer
from .repo import CategoryRepo,ProductRepo
TEMPLATE_ROOT="snapp/"
LAYOUT_PARENT="phoenix/layout.html"


def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        root_categories=CategoryRepo(request=request).list(root=True)
        context['root_categories']=root_categories
        root_categories_s=json.dumps(CategorySerializer(root_categories,many=True).data)
        context['root_categories_s']=root_categories_s
        return render(request,TEMPLATE_ROOT+"index.html",context)

class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)

        category=CategoryRepo(request=request).category(*args, **kwargs)
        context['category']=category

        categories=CategoryRepo(request=request).list(parent_id=category.id)
        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s

        products=category.products.all()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"category.html",context)
from market.views import ShopRepo,ShopSerializer,CustomerRepo
 

class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        context['product']=product
        
        
        me_customer=CustomerRepo(request=request).me

        if me_customer is not None:
            customer_shops=ShopRepo(request=request).list(product_id=product.id,level=me_customer.level)
            customer_shops_s=json.dumps(ShopSerializer(customer_shops,many=True).data)
            context["customer_shops"]=customer_shops
            context["customer_shops_s"]=customer_shops_s
        
        return render(request,TEMPLATE_ROOT+"product.html",context)