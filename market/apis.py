import json
from unicodedata import category
from django.http import JsonResponse
from rest_framework.views import APIView
from accounting.repo import ProductRepo
from accounting.serializers import InvoiceSerializer
from core.constants import FAILED,SUCCEED
from market.forms import *
from market.serializers import CartLineSerializer, CategorySerializer, CategorySerializerForApi, ProductSerializer,ProductSerializerForApi, ShopSerializer
from market.repo import CartLineRepo, CartRepo, CategoryRepo, ShopRepo
from utility.log import leolog
class AddCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        add_category_form=AddCategoryForm(request.POST)
        if add_category_form.is_valid():
            category=CategoryRepo(request=request).add_category(**add_category_form.cleaned_data)
            if category is not None:
                context['category']=CategorySerializer(category).data
                context['result']=SUCCEED
        return JsonResponse(context)

class AddToCartApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        AddToCartForm_=AddToCartForm(request.POST)
        if AddToCartForm_.is_valid():
            (result,cart_line,message)=CartRepo(request=request).add_to_cart(**AddToCartForm_.cleaned_data)
            if result==SUCCEED:
                context['cart_line']=CartLineSerializer(cart_line).data
                context['result']=SUCCEED
            else:
                context['message']=message
        return JsonResponse(context)




class CheckoutApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        log=2
        checkout_form=CheckoutForm(request.POST)
        if checkout_form.is_valid():
            log=3
            cd=checkout_form.cleaned_data
            cd['cart_lines']=json.loads(cd['cart_lines'])
            market_invoices,result,message=CartRepo(request=request).checkout(
                **cd
            )
            if result ==SUCCEED:
                # shops=ProductRepo(request=request).product(pk=product_id).shop_set.all()
                context['market_invoices']=InvoiceSerializer(market_invoices,many=True).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)



 


class AddShopApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        log=2
        add_shop_form=AddShopForm(request.POST)
        if add_shop_form.is_valid():
            log=3
            cd=add_shop_form.cleaned_data
            cd['specifications']=json.loads(cd['specifications'])
            shop=ShopRepo(request=request).add_shop(
                **cd
            )
            if shop is not None:
                # shops=ProductRepo(request=request).product(pk=product_id).shop_set.all()
                context['shop']=ShopSerializer(shop).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)




class AddProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        add_product_form=AddProductForm(request.POST)
        if add_product_form.is_valid():
            (result,product,message)=ProductRepo(request=request).add_product(**add_product_form.cleaned_data)
            if product is not None:
                category=CategoryRepo(request=request).category(pk=add_product_form.cleaned_data['category_id'])
                if category is not None:
                    category.products.add(product)
                context['product']=ProductSerializer(product).data
                context['result']=SUCCEED
            else:
                context['message']=message
        return JsonResponse(context)



class CategoryApi(APIView):
    def get(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        category=CategoryRepo(request=request).category(*args, **kwargs)
        categories=category.childs.all()
        categories=CategorySerializerForApi(categories,many=True).data
        context['category']=CategorySerializerForApi(category).data
        context['categories']=categories
        products=category.products.all()
        products=ProductSerializerForApi(products,many=True).data
        context['products']=products
        context['result']=SUCCEED
        return JsonResponse(context)

class CategoriesApi(APIView):
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
        categories=category.childs.all()
        categories=CategorySerializerForApi(categories,many=True).data
        context['categories']=categories
        context['category']=CategorySerializerForApi(category).data
        context['result']=SUCCEED
        return JsonResponse(context)
