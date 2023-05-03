from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext
from .forms import *
import json
from .serializers import CategorySerializer,ProductSerializer,MenuSerializer,ShopSerializer
from .repo import CategoryRepo,ProductRepo,MenuRepo
from market.views import ShopRepo,CustomerRepo

TEMPLATE_ROOT="snapp/"
LAYOUT_PARENT="phoenix/layout.html"


def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['title']="svdgsfdadg"
        root_categories=CategoryRepo(request=request).list(root=True)
        context['root_categories']=root_categories
        root_categories_s=json.dumps(CategorySerializer(root_categories,many=True).data)
        context['root_categories_s']=root_categories_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    
class MenusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menus=MenuRepo(request=request).list(root=True)
        context['menus']=menus
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus_s']=menus_s
        if request.user.has_perm(APP_NAME+".add_menu"):
            context['add_menu_form']=AddMenuForm()
        return render(request,TEMPLATE_ROOT+"menus.html",context)
    
class MenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menu=MenuRepo(request=request).menu(*args, **kwargs)
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s
        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s
        context['shops']=shops
        return render(request,TEMPLATE_ROOT+"menu.html",context)
    
class CategoriesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        root_categories=CategoryRepo(request=request).list(root=True)
        context['root_categories']=root_categories
        root_categories_s=json.dumps(CategorySerializer(root_categories,many=True).data)
        context['root_categories_s']=root_categories_s
        return render(request,TEMPLATE_ROOT+"categories.html",context)

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