from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render,reverse
from django.utils import timezone
from requests import request
from accounting.apis import EditInvoiceApi
from accounting.enums import FinancialBalanceTitleEnum, PaymentMethodEnum, TransactionStatusEnum
from core.constants import CURRENCY, FAILED, SUCCEED
from core.enums import UnitNameEnum
from core.utils import app_is_installed
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View
from guarantee.serializers import GuaranteeSerializer

from utility.calendar import PersianCalendar
from utility.excel import ReportSheet,ReportWorkBook, get_style
from warehouse.repo import WareHouseRepo, WareHouseSheetRepo
from warehouse.serializers import WareHouseSerializer, WareHouseSheetSerializer
from accounting.apps import APP_NAME
from accounting.repo import AssetRepo, InvoiceLineRepo,AccountRepo,FinancialBalanceRepo, ChequeRepo, PaymentRepo, PriceRepo, ProductRepo,ServiceRepo,FinancialDocumentRepo,InvoiceRepo, TransactionRepo
from accounting.serializers import AccountSerializer, AssetSerializer, FinancialBalanceSerializer, InvoiceFullSerializer,InvoiceLineSerializer,ChequeSerializer, InvoiceSerializer, PaymentSerializer, PriceSerializer, ProductSerializer,ServiceSerializer,FinancialDocumentForAccountSerializer,FinancialDocumentSerializer, TransactionSerializer
from accounting.forms import *
import json
from phoenix.server_settings import phoenix_apps
from core.repo import ParameterRepo
from accounting.enums import ParameterAccountingEnum
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "accounting/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


def get_add_payment_context(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_payment"):
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
        context['accounts']=accounts
        context['add_payment_form']=AddPaymentForm()
    return context
    
def add_from_accounts_context(request):
    context={}
    accounts=AccountRepo(request=request).list()
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['accounts']=accounts
    context['accounts_s']=accounts_s
    return context


def get_edit_invoice_context(request,*args, **kwargs):
    context={}
    invoice=kwargs['invoice'] 
    customers=AccountRepo(request=request).list(all=True)
    context['customers']=customers

    stores=AccountRepo(request=request).list()
    context['stores']=stores
        
    products=ProductRepo(request=request).list()
    context['products']=products
    context['products_s']=json.dumps(ProductSerializer(products,many=True).data)



    
    services=ServiceRepo(request=request).list()
    context['services']=services
    context['services_s']=json.dumps(ServiceSerializer(services,many=True).data)

    context['unit_names']=(u[0] for u in UnitNameEnum.choices)
    context['invoice_statuses']=(u[0] for u in TransactionStatusEnum.choices)
    context['invoice_payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
    
    return context
    

def get_invoice_context(request,*args, **kwargs):
    context={}
    invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
    context['invoice']=invoice
    if invoice is None:
        mv=MessageView(request=request)
        mv.title="چنین فاکتوری یافت نشد."
        return mv.response()

    context.update(get_transaction_context(request=request,transaction=invoice))
    invoice_lines=invoice.invoice_lines()
    invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
    context['invoice_lines_s']=invoice_lines_s
    context['invoice_s']=json.dumps(InvoiceFullSerializer(invoice).data)
    
    
    if app_is_installed('guarantee'):
        from guarantee.repo import GuaranteeRepo
        guarantees=GuaranteeRepo(request=request).list(invoice_id=invoice.id)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s

    
    # warehouse_sheets=[]
    if app_is_installed('warehouse'):
        from warehouse.repo import WareHouseSheetRepo
        warehouse_sheets=WareHouseSheetRepo(request=request).list(invoice_id=invoice.id)
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s



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

def get_account_context(request,*args, **kwargs):
    context={}
    if 'account' in kwargs:
        account=kwargs['account']
    else:
        account=AccountRepo(request=request).account(*args, **kwargs)
    if account is None:
        raise Http404
    context['account']=account

    invoices=account.invoices()
    context['invoices']=invoices
    context['invoices_s']=json.dumps(InvoiceSerializer(invoices,many=True).data)
    count=int(ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterAccountingEnum.COUNT_OF_ITEM_PER_PAGE,default=10).value)
    count=kwargs['count'] if 'count' in kwargs else count
    financial_documents=FinancialDocumentRepo(request=request).list(account_id=account.id)[:count]
    context['financial_documents']=financial_documents
    context['financial_documents_s']=json.dumps(FinancialDocumentForAccountSerializer(financial_documents,many=True).data)

    financial_balances=FinancialBalanceRepo(request=request).list(account_id=account.id)
    context['financial_balances']=financial_balances
    context['financial_balances_s']=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)



    if request.user.has_perm(APP_NAME+".add_payment"):
        context.update(get_add_payment_context(request=request))



    transactions=TransactionRepo(request=request).list(account_id=account.id)[:count]
    context['transactions']=transactions
    context['transactions_s']=json.dumps(TransactionSerializer(transactions,many=True).data)

    payments=PaymentRepo(request=request).list(account_id=account.id)[:count]
    context['payments']=payments
    context['payments_s']=json.dumps(PaymentSerializer(payments,many=True).data)
    
    return context

def get_transaction_context(request,*args, **kwargs):
    context={}
    if 'transaction' in kwargs:
        transaction=kwargs['transaction']
    else:
        transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
    if transaction is None:
        mv=MessageView(request=request)
        mv.title="چنین تراکنشی یافت نشد."
        return mv.response()
    context['transaction']=transaction
    context.update(PageContext(request=request,page=transaction))

    financial_documents=FinancialDocumentRepo(request=request).list(transaction_id=transaction.id)
    financial_documents=transaction.financialdocument_set.all()
    context['financial_documents']=financial_documents
    context['financial_documents_s']=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
            

    financial_balances=FinancialBalanceRepo(request=request).list(transaction_id=transaction.id)
    context['financial_balances']=financial_balances
    financial_balances_s=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)
    context['financial_balances_s']=financial_balances_s

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
    if product is None:
        mv=MessageView(request=request)
        mv.title="چنین کالایی یافت نشد."
        return mv.response()
    
    context=get_product_or_service_context(request=request,item=product,*args, **kwargs)

    # invoices
    invoices=InvoiceRepo(request=request).list(product_id=product.id)
    context['invoices']=invoices
    invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
    context['invoices_s']=invoices_s


    if app_is_installed('guarantee'):
        from guarantee.repo import GuaranteeRepo
        guarantees=GuaranteeRepo(request=request).list(product_id=product.id)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s

    
    #warehouse availables , warehouse sheets
    warehouse_app_is_installed= app_is_installed('warehouse')
    if warehouse_app_is_installed:
        from warehouse.repo import WareHouseSheetRepo
        from warehouse.enums import WareHouseSheetStatusEnum
        ware_house_sheet_repo=WareHouseSheetRepo(request=request)
        products=[product]
        ware_houses=WareHouseRepo(request=request).list()
        availables_list=[]
        warehouse_sheets=ware_house_sheet_repo.list(product_id=product.id).filter(status=WareHouseSheetStatusEnum.DONE)

        for ware_house in ware_houses:    
            for product in products:    
                line=warehouse_sheets.filter(ware_house=ware_house).first()
                if line is not None:
                    list_item={'product':{'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}}
                    list_item['available']=line.available
                    list_item['unit_name']=line.unit_name
                    list_item['ware_house']=WareHouseSerializer(line.ware_house).data
                    availables_list.append(list_item)
        context['availables_list']=json.dumps(availables_list)
     
        warehouse_sheets=ware_house_sheet_repo.list(product_id=product.id)
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s
 


    return context

def get_service_context(request,*args, **kwargs):
    context=get_product_or_service_context(request=request,*args, **kwargs)
    return context

def get_search_form_context(request,*args, **kwargs):
    context={}
    accounts=AccountRepo(request=request).list(*args, **kwargs)
    context['accounts']=accounts
    context['search_form']=SearchForm()

    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)



class SearchView(View):
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context['search_for']=search_for

            accounts=AccountRepo(request=request).list(search_for=search_for)
            context['accounts']=accounts
            context['accounts_s']=json.dumps(AccountSerializer(accounts,many=True).data)

            invoices=InvoiceRepo(request=request).list(search_for=search_for)
            context['invoices']=invoices
            context['invoices_s']=json.dumps(InvoiceSerializer(invoices,many=True).data)

            financial_balances=FinancialBalanceRepo(request=request).list(search_for=search_for)
            context['financial_balances']=financial_balances
            context['financial_balances_s']=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)

            payments=PaymentRepo(request=request).list(search_for=search_for)
            context['payments']=payments
            context['payments_s']=json.dumps(PaymentSerializer(payments,many=True).data)

            financial_documents=FinancialDocumentRepo(request=request).list(search_for=search_for)
            context['financial_documents']=financial_documents
            context['financial_documents_s']=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
            
            transactions=TransactionRepo(request=request).list(search_for=search_for)
            context['transactions']=transactions
            context['transactions_s']=json.dumps(TransactionSerializer(transactions,many=True).data)


        return render(request,TEMPLATE_ROOT+"search.html",context)


class SearchJsonView(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            cd1=search_form.cleaned_data
            cd={}
            cd['start_date']=PersianCalendar().to_gregorian(cd1['start_date'])
            cd['end_date']=PersianCalendar().to_gregorian(cd1['end_date'])
            cd['search_for']=cd1['search_for']
            cd['account_id']=cd1['account_id']

            accounts=AccountRepo(request=request).list(cd)
            context['accounts']=(AccountSerializer(accounts,many=True).data)

            invoices=InvoiceRepo(request=request).list(cd)
            context['invoices']=(InvoiceSerializer(invoices,many=True).data)

            financial_balances=FinancialBalanceRepo(request=request).list(kwargs=cd)
            context['financial_balances']=(FinancialBalanceSerializer(financial_balances,many=True).data)

            payments=PaymentRepo(request=request).list(cd)
            context['payments']=(PaymentSerializer(payments,many=True).data)

            financial_documents=FinancialDocumentRepo(request=request).list(**cd)
            context['financial_documents']=(FinancialDocumentSerializer(financial_documents,many=True).data)
            
            transactions=TransactionRepo(request=request).list(cd)
            context['transactions']=(TransactionSerializer(transactions,many=True).data)
            context['result']=SUCCEED
        return JsonResponse(context)


class FinancialBalancesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_balances=FinancialBalanceRepo(request=request).list(*args, **kwargs)
        context['financial_balances']=financial_balances
        context['financial_balances_s']=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)
        return render(request,TEMPLATE_ROOT+"financial-balances.html",context)
class FinancialBalanceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_balance=FinancialBalanceRepo(request=request).financial_balance(*args, **kwargs)

        context['financial_balance']=financial_balance
        return render(request,TEMPLATE_ROOT+"financial-balance.html",context)

class InvoiceExcelView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,invoice_line in enumerate(invoice.invoice_lines(),1):
            line={
                'ردیف':i,
                'title':invoice_line.product_or_service.title,
                'آدرس':invoice_line.quantity,      
                'unit_name':invoice_line.unit_name,      
                'unit_price':invoice_line.unit_price,      
                'line_total':invoice_line.line_total(),      
            }
            lines.append(line)
               
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'Page.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        report_work_book.add_sheet(
             data=lines,
            start_row=3,
            start_col=1,
            table_has_header=False,
            table_headers=None,
            style=style,
            sheet_name='links',
        )
        lines=[]
        for i,document in enumerate([{'title':'dddd','get_download_url':'7654erftgh'}],1):
            line={
                'ردیف':i,
                'عنوان ':document['title'],
                'آدرس':document['get_download_url'],          
            }
            lines.append(line)
            

        # sheet2=ReportSheet(
        #     # data=json.dumps(DocumentSerializer(page.documents.all(),many=True).data),
        #     data=lines,
        #     current_row=3,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='docs',
           
        # )
        report_work_book.add_sheet(
              data=lines,
            start_row=3,
            table_has_header=False,
            table_headers=None,
            style=style,
            sheet_name='docs',
        )
            
        file_name=f"""{date.replace('/','').replace(':','')}   Page {1}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

class NewInvoiceView(View):
    def get(self,request,*args, **kwargs):
        invoice=InvoiceRepo(request=request).create_invoice(*args, **kwargs)
        return redirect(invoice.get_absolute_url())


 
class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="چنین فاکتوری یافت نشد."
            return mv.response()
        context.update(get_invoice_context(request=request,*args, **kwargs))
        # context['no_navbar']=True
        # context['no_footer']=True
        return render(request,TEMPLATE_ROOT+"invoice.html",context)
class InvoicePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        currency=CURRENCY
        context['TUMAN']=True
        context['RIAL']=False
        if 'currency' in kwargs:
            currency=kwargs['currency']
            if currency=='r':
                context['TUMAN']=False
                context['RIAL']=True
                from core.constants import RIAL
                context['CURRENCY']=RIAL

        context['no_footer']=True
        context['no_navbar']=True
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)
class InvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list(*args, **kwargs)
        context['invoices']=invoices
        context['expand_invoices']=True
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices_s']=invoices_s
        return render(request,TEMPLATE_ROOT+"invoices.html",context)
class InvoiceEditView(View):
    def post(self,request,*args, **kwargs):
        return EditInvoiceApi().post(request=request,*args, **kwargs)
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        invoice=context['invoice']
        context.update(get_edit_invoice_context(request=request,invoice=invoice,*args, **kwargs))
        
        return render(request,TEMPLATE_ROOT+"invoice-edit.html",context)
class InvoiceLineView(View):
    def post(self,request,*args, **kwargs):
        return EditInvoiceApi().post(request=request,*args, **kwargs)
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice_line=InvoiceLineRepo(request=request).invoice_line(*args, **kwargs)
        context['invoice_line']=invoice_line

            
        
        if app_is_installed('guarantee'):
            from guarantee.repo import GuaranteeRepo
            guarantees=GuaranteeRepo(request=request).list(invoice_line_id=invoice_line.id)
            context['guarantees']=guarantees
            guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
            context['guarantees_s']=guarantees_s

        
        # warehouse_sheets=[]
        if app_is_installed('warehouse'):
            from warehouse.enums import WareHouseSheetDirectionEnum
            from warehouse.repo import WareHouseSheetRepo,WareHouseRepo
            from warehouse.forms import AddWarehouseSheetForm
            warehouse_sheets=WareHouseSheetRepo(request=request).list(invoice_line_id=invoice_line.id)
            warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
            context['warehouse_sheets_s']=warehouse_sheets_s
            if request.user.has_perm('warehouse.add_warehousesheet'):
                context['add_ware_house_sheet_form']=AddWarehouseSheetForm()
                ware_houses=WareHouseRepo(request=request).list()
                context['directions']=(direction[0] for direction in WareHouseSheetDirectionEnum.choices)
                context['ware_houses']=ware_houses

        # context['add_ware_house_sheet_form']=AddWarehouseSheetForm()

        return render(request,TEMPLATE_ROOT+"invoice-line.html",context)

class TransactionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        context.update(get_transaction_context(request=request,*args, **kwargs))
        if context['transaction'] is None:
            mv=MessageView(request=request)
            mv.title="چنین تراکنشی یافت نشد."
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
class TransactionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
class TransactionsPrintView(View):
    def post(self,request,*args, **kwargs):
        transactions_print_form=TransactionsPrintForm(request.POST)
        if transactions_print_form.is_valid():
            context=getContext(request=request)
            cd=transactions_print_form.cleaned_data
            transactions=cd['transactions']
            context['transactions']=transactions
            context['title']=cd['title']
            context['no_footer']=True
            context['no_navbar']=True
            return render(request,TEMPLATE_ROOT+"transactions-print.html",context)


class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form']=AddProductForm()
        return render(request,TEMPLATE_ROOT+"products.html",context)
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        print('warehouse_app_is_installed')
        print(context['warehouse_app_is_installed'])
        if product is None:
            mv=MessageView(request=request)
            mv.title="چنین کالایی یافت نشد."
        context.update(get_product_context(request=request,product=product))
        return render(request,TEMPLATE_ROOT+"product.html",context)


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        if request.user.has_perm(APP_NAME+".add_service"):
            context['add_service_form']=AddServiceForm()
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
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        create_account_form=CreateAccountForm(request.POST)
        if create_account_form.is_valid():
            cd=create_account_form.cleaned_data
            profile_id=cd['profile_id']
            account=AccountRepo(request=request).account(profile_id=profile_id)
            if account is not None:
                context['account']=AccountSerializer(account).data
                context['result']=SUCCEED

        return JsonResponse(context)

        
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        account=AccountRepo(request=request).account(*args, **kwargs)
        context['account']=account

        context.update(get_account_context(request=request,account=account))
        return render(request,TEMPLATE_ROOT+"account.html",context)      
class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['accounts']=accounts
        context['expand_accounts']=True
        if request.user.has_perm(APP_NAME+".add_account"):
            context['add_account_form']=AddAccountForm()
        return render(request,TEMPLATE_ROOT+"accounts.html",context)

     

class PaymentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        payments=PaymentRepo(request=request).list(*args, **kwargs)
        context['payments']=payments
        context['expand_payments']=True

        context['payments_s']=json.dumps(PaymentSerializer(payments,many=True).data)
        if request.user.has_perm(APP_NAME+".add_payment"):
            context.update(get_add_payment_context(request=request))
        return render(request,TEMPLATE_ROOT+"payments.html",context)
class PaymentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        payment=PaymentRepo(request=request).payment(*args, **kwargs)
        context['payment_s']=json.dumps(PaymentSerializer(payment).data)
        context['payment']=payment
        context.update(get_transaction_context(request=request,transaction=payment))
        return render(request,TEMPLATE_ROOT+"payment.html",context)

class FinancialDocumentsView(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        search_accounting_form=SearchAccountingForm(request.POST)
        if search_accounting_form.is_valid():
            cd=search_accounting_form.cleaned_data
            start_date=cd['start_date']
            end_date=cd['end_date']
            search_for=cd['search_for']
            account_id=cd['account_id']
            profile_id=cd['profile_id']
            financial_documents=FinancialDocumentRepo(request=request).list(
                start_date=start_date,
                end_date=end_date,
                search_for=search_for,
                account_id=account_id,
                profile_id=profile_id
                )
            financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
            context['financial_documents']=financial_documents_s
            context['result']=SUCCEED
        return JsonResponse(context)

    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_documents=FinancialDocumentRepo(request=request).list(*args, **kwargs)
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s
        rest=0
        context['rest']=rest

        context.update(get_search_form_context(request=request))
        return render(request,TEMPLATE_ROOT+"financial-documents.html",context)
class FinancialDocumentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_document=FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        financial_document.normalize_balances()

        context['financial_document']=financial_document
        financial_balances=FinancialBalanceRepo(request=request).list(financial_document_id=financial_document.id)
        context['financial_balances']=financial_balances
        if request.user.has_perm(APP_NAME+".add_financialdocument"):
            context['add_financial_balance_form']=AddFinancialBalanceForm()
            context['financial_balance_title_enum']=(cc[0] for cc in FinancialBalanceTitleEnum.choices)
        return render(request,TEMPLATE_ROOT+"financial-document.html",context)

class AssetsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        assets=AssetRepo(request=request).list(*args, **kwargs)
        context['assets']=assets
        assets_s=json.dumps(AssetSerializer(assets,many=True).data)
        context['assets_s']=assets_s
        return render(request,TEMPLATE_ROOT+"assets.html",context)

class AssetView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        asset=AssetRepo(request=request).asset(*args, **kwargs)
        context['asset']=asset
        context.update(PageContext(request=request,page=asset))
        return render(request,TEMPLATE_ROOT+"asset.html",context)
