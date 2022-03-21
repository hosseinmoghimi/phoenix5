from django.http import Http404
from django.shortcuts import render,reverse
from core.enums import UnitNameEnum
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View
from .apps import APP_NAME
from .repo import AccountRepo,FinancialBalanceRepo, ChequeRepo, PriceRepo, ProductRepo,ServiceRepo,FinancialDocumentRepo,InvoiceRepo, TransactionRepo
from .serializers import InvoiceLineSerializer,ChequeSerializer, ProductSerializer,ServiceSerializer,FinancialDocumentForAccountSerializer,FinancialDocumentSerializer
from .forms import *
import json


LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "accounting/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context

def get_invoice_context(request,*args, **kwargs):
    context={}
    invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
    context.update(get_transaction_context(request=request,transaction=invoice))
    context['invoice']=invoice

    invoice_lines=invoice.invoice_lines()
    invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
    context['invoice_lines_s']=invoice_lines_s
    return context

def get_price_app_context(request,*args, **kwargs):
    context={}
    accounts=AccountRepo(request=request).my_list(*args, **kwargs)
    context['accounts']=accounts
    if 'items' in kwargs:
        items=kwargs['items']
    else:
        items=[]
    context['items']=items
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context['unit_names']=unit_names
    prices=PriceRepo(request=request).list(item_id=items[0].id)
    context['prices']=prices
    return context

def get_transaction_context(request,*args, **kwargs):
    context={}
    if 'transaction' in kwargs:
        transaction=kwargs['transaction']
    else:
        transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
    if transaction is None:
        raise Http404
    context['transaction']=transaction
    context.update(PageContext(request=request,page=transaction))
    return context

def get_product_or_service_context(request,*args, **kwargs):
    context={}
    if 'product_or_service' in kwargs:
        product_or_service=kwargs['product_or_service']
    if 'product' in kwargs:
        product_or_service=kwargs['product']
        context['product']=product_or_service
    if 'item' in kwargs:
        product_or_service=kwargs['item']
    if 'service' in kwargs:
        product_or_service=kwargs['service']
        context['service']=product_or_service

    context['product_or_service']=product_or_service
    context.update(PageContext(request=request,page=product_or_service))
    context.update(get_price_app_context(request=request,items=[product_or_service]))

    return context

def get_product_context(request,*args, **kwargs):
    product=ProductRepo(request=request).product(*args, **kwargs)
    context=get_product_or_service_context(request=request,item=product,*args, **kwargs)
    return context

def get_service_context(request,*args, **kwargs):
    context=get_product_or_service_context(request=request,*args, **kwargs)
    return context



class FinancialBalancesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_balances=FinancialBalanceRepo(request=request).list(*args, **kwargs)
        context['financial_balances']=financial_balances
        return render(request,TEMPLATE_ROOT+"financial-balances.html",context)


class InvoiceShowView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        context['no_navbar']=True
        context['no_footer']=True
        return render(request,TEMPLATE_ROOT+"invoice-show.html",context)
    
class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        return render(request,TEMPLATE_ROOT+"invoice.html",context)
class InvoicePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        context['no_footer']=True
        context['no_nav_bar']=True
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)
class InvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list(*args, **kwargs)
        context['invoices']=invoices
        return render(request,TEMPLATE_ROOT+"invoices.html",context)


class TransactionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_transaction_context(request=request,*args, **kwargs))
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
class TransactionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        return render(request,TEMPLATE_ROOT+"transactions.html",context)


class EditInvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        
        return render(request,TEMPLATE_ROOT+"edit-invoice.html",context)
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
        context.update(get_product_context(request=request,product=product))
        return render(request,TEMPLATE_ROOT+"product.html",context)


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
        context.update(get_service_context(request=request,service=service))
        return render(request,TEMPLATE_ROOT+"service.html",context)
        

class ChequesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheques=ChequeRepo(request=request).list(*args, **kwargs)
        context['cheques']=cheques
        cheques_s=json.dumps(ChequeSerializer(cheques,many=True).data)
        context['cheques_s']=cheques_s
        if request.user.has_perm(APP_NAME+".add_cheque"):
            context['add_cheque_form']=AddChequeForm()
        return render(request,TEMPLATE_ROOT+"cheques.html",context)
class ChequeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheque=ChequeRepo(request=request).cheque(*args, **kwargs)
        context['cheque']=cheque
        cheque_s=json.dumps(ChequeSerializer(cheque).data)
        context['cheque_s']=cheque_s 
        context.update(get_transaction_context(request=request,transaction=cheque))
        return render(request,TEMPLATE_ROOT+"cheque.html",context)
    

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

        financial_balances=FinancialBalanceRepo(request=request).list(account_id=account.id)
        context['financial_balances']=financial_balances

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
        financial_balances=FinancialBalanceRepo(request=request).list(financial_document_id=financial_document.id)
        context['financial_balances']=financial_balances
        return render(request,TEMPLATE_ROOT+"financial-document.html",context)
