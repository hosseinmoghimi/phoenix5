from django.shortcuts import render,reverse
from accounting.utils import init_sub_accounts
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View
from .apps import APP_NAME
from .repo import AccountRepo, ProductRepo,ServiceRepo,FinancialDocumentRepo
from .serializers import ProductSerializer,ServiceSerializer,FinancialDocumentForAccountSerializer,FinancialDocumentSerializer
import json


LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "accounting/"


def getContext(request, *args, **kwargs):
    init_sub_accounts(delete_all=False)
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)

class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"products.html",context)

class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        context.update(PageContext(request=request,page=product))
        context['product']=product
        return render(request,TEMPLATE_ROOT+"product.html",context)



class AccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        account=AccountRepo(request=request).account(*args, **kwargs)
        context['account']=account
        financial_documents=FinancialDocumentRepo(request=request).list(account_id=account.id)
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentForAccountSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s
        rest=0
        context['rest']=rest
        return render(request,TEMPLATE_ROOT+"account.html",context)

        
class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['accounts']=accounts
        return render(request,TEMPLATE_ROOT+"accounts.html",context)

class FinancialDocumentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_documents=FinancialDocumentRepo(request=request).list(*args, **kwargs)
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s
        rest=0
        context['rest']=rest
        return render(request,TEMPLATE_ROOT+"financial-documents.html",context)


class FinancialDocumentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_document=FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        context['financial_document']=financial_document
        return render(request,TEMPLATE_ROOT+"financial-document.html",context)

class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        return render(request,TEMPLATE_ROOT+"services.html",context)

class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service=ServiceRepo(request=request).service(*args, **kwargs)
        context.update(PageContext(request=request,page=service))
        context['service']=service
        return render(request,TEMPLATE_ROOT+"service.html",context)