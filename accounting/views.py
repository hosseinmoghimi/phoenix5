from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render,reverse
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer
from phoenix.constants import TUMAN
from warehouse.serializers import WareHouseSheetSerializer
from accounting import apis
from accounting.apis import EditInvoiceApi
from accounting.enums import CostTypeEnum, FinancialBalanceTitleEnum, PaymentMethodEnum, TransactionStatusEnum
from core.constants import CURRENCY, FAILED, SUCCEED
from core.enums import UnitNameEnum
from core.utils import app_is_installed
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View

from utility.calendar import PersianCalendar
from utility.excel import ReportSheet,ReportWorkBook, get_style
from accounting.apps import APP_NAME
from accounting.repo import BankRepo,AssetRepo, CategoryRepo, CostRepo,BankAccountRepo, DoubleTransactionRepo, InvoiceLineRepo,AccountRepo,FinancialBalanceRepo, ChequeRepo, PaymentRepo, PriceRepo,  ProductRepo,ServiceRepo,FinancialDocumentRepo,InvoiceRepo, TransactionRepo
from accounting.serializers import ProductOrServiceUnitNameSerializer, ProductSpecificationSerializer,CategorySerializer, InvoiceLineWithInvoiceSerializer,AccountSerializer, AccountSerializerFull, AssetSerializer, BankAccountSerializer, BankSerializer, CostSerializer, FinancialBalanceSerializer, InvoiceFullSerializer,InvoiceLineSerializer,ChequeSerializer, InvoiceSerializer, PaymentSerializer, PriceSerializer,  ProductSerializer,ServiceSerializer,FinancialDocumentForAccountSerializer,FinancialDocumentSerializer, TransactionSerializer
from accounting.forms import *
import json
from utility.log import leolog
from phoenix.server_settings import phoenix_apps
from core.repo import ParameterRepo
from accounting.enums import ParameterAccountingEnum
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "accounting/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['me_account']=AccountRepo(request=request).me
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context

def add_product_context(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_product"):
        context['add_product_form']=AddProductForm()
        context['unit_names']=(unit_name[0] for unit_name in UnitNameEnum.choices)
    return context

def add_transaction_context(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_transaction"):
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['transaction_statuses']=(u[0] for u in TransactionStatusEnum.choices)
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
        context['accounts']=accounts
    return context
def get_add_payment_context(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_payment"):
        context.update(add_transaction_context(request=request))
        context['add_payment_form']=AddPaymentForm()
    return context
    
def get_add_cost_context(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_cost"):
        context.update(add_transaction_context(request=request))
        context['cost_types']=(u[0] for u in CostTypeEnum.choices)
        context['add_cost_form']=AddCostForm()
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
        from guarantee.serializers import GuaranteeSerializer
        guarantees=GuaranteeRepo(request=request).list(invoice_id=invoice.id)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s

    
    # warehouse_sheets=[]
    if app_is_installed('warehouse'):
        from warehouse.repo import WareHouseSheetRepo
        from warehouse.serializers import WareHouseSheetSerializer
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
    context['prices_s']=json.dumps(PriceSerializer(prices,many=True).data)
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

    invoices=InvoiceRepo(request=request).list(account_id=account.id)
    context['invoices']=invoices
    context['invoices_s']=json.dumps(InvoiceSerializer(invoices,many=True).data)
    count=int(ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterAccountingEnum.COUNT_OF_ITEM_PER_PAGE,default=100).value)
    count=kwargs['count'] if 'count' in kwargs else count
    financial_documents=FinancialDocumentRepo(request=request).list(account_id=account.id).order_by('transaction__transaction_datetime')[:count]
    context['financial_documents']=financial_documents
    context['financial_documents_s']=json.dumps(FinancialDocumentForAccountSerializer(financial_documents,many=True).data)

    financial_balances=FinancialBalanceRepo(request=request).list(account_id=account.id)
    context['financial_balances']=financial_balances
    context['financial_balances_s']=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)


    costs=CostRepo(request=request).list(account_id=account.id)
    context['costs']=costs
    context['costs_s']=json.dumps(CostSerializer(costs,many=True).data)





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



    if not transaction.editable and request.user.has_perm(APP_NAME+".change_transaction"):
        context['roll_back_transaction_form']=RollBackTransactionForm()
        
    return context

def get_double_transaction_context(request,*args, **kwargs):
    context={}
    if 'double_transaction' in kwargs:
        transaction=kwargs['double_transaction']
    else:
        double_transaction=DoubleTransactionRepo(request=request).double_transaction(*args, **kwargs)
    context['double_transaction']=double_transaction
    
    transactions=[double_transaction.employer_transaction,double_transaction.middle_transaction]
    context['transactions']=transactions
    transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
    context['transactions_s']=transactions_s

    context.update(PageContext(request=request,page=double_transaction))
    if double_transaction.employer_transaction is not None:

        financial_documents=FinancialDocumentRepo(request=request).list(transaction_id=double_transaction.employer_transaction.id)
        financial_documents=double_transaction.employer_transaction.financialdocument_set.all()
        context['financial_documents']=financial_documents
        context['financial_documents_s']=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
                

        financial_balances=FinancialBalanceRepo(request=request).list(transaction_id=double_transaction.employer_transaction.id)
        context['financial_balances']=financial_balances
        financial_balances_s=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)
        context['financial_balances_s']=financial_balances_s



        if not double_transaction.employer_transaction.editable and request.user.has_perm(APP_NAME+".change_transaction"):
            context['roll_back_transaction_form']=RollBackTransactionForm()
            
            



    if double_transaction.middle_transaction is not None:

        financial_documents=FinancialDocumentRepo(request=request).list(transaction_id=double_transaction.middle_transaction.id)
        financial_documents=double_transaction.middle_transaction.financialdocument_set.all()
        context['financial_documents']=financial_documents
        context['financial_documents_s']=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
                

        financial_balances=FinancialBalanceRepo(request=request).list(transaction_id=double_transaction.middle_transaction.id)
        context['financial_balances']=financial_balances
        financial_balances_s=json.dumps(FinancialBalanceSerializer(financial_balances,many=True).data)
        context['financial_balances_s']=financial_balances_s



        if not double_transaction.middle_transaction.editable and request.user.has_perm(APP_NAME+".change_transaction"):
            context['roll_back_transaction_form']=RollBackTransactionForm()
            
            


  
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
    
    product_or_service_unit_names=product_or_service.unit_names()
    context['product_or_service_unit_names']=product_or_service_unit_names
    product_or_service_unit_names_s=json.dumps(ProductOrServiceUnitNameSerializer(product_or_service_unit_names,many=True).data)
    context['product_or_service_unit_names_s']=product_or_service_unit_names_s

    # invoices
    if request.user.has_perm(APP_NAME+".view_invoice"):
        invoices=InvoiceRepo(request=request).list(product_or_service_id=product_or_service.id)
        invoice_lines=InvoiceLineRepo(request=request).list(product_or_service_id=product_or_service.pk)
    else:    
        me_account=AccountRepo(request=request).me
        invoices=InvoiceRepo(request=request).list(product_or_service_id=product_or_service.id,account_id=me_account.id)
        invoice_lines=InvoiceLineRepo(request=request).list(product_or_service_id=product_or_service.pk,account_id=me_account.id)
        
    context['invoices']=invoices
    invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
    context['invoices_s']=invoices_s

    # invoice_lines
    invoice_lines=InvoiceLineRepo(request=request).list(product_or_service_id=product_or_service.pk)
    context['invoice_lines']=invoice_lines
    # invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
    # context['invoice_lines_s']=invoice_lines_s


    #item_categories
    item_categories=product_or_service.category_set.all()
    context['item_categories']=item_categories
    context['item_categories_s']=json.dumps(CategorySerializer(item_categories,many=True).data)
    if request.user.has_perm(APP_NAME+".change_productorservice"):
        all_categories=CategoryRepo(request=request).list().order_by('title')
        context['all_categories']=all_categories
        context['all_categories_s']=json.dumps(CategorySerializer(all_categories,many=True).data)
        context['add_item_category_form']=AddItemCategoryForm()

        # for adding unit name
        context['all_unit_names_for_add_product_or_service_form']=(u[0] for u in UnitNameEnum.choices)
        context['add_product_or_service_unit_name_form']=AddProductOrServiceUnitNameForm()
    return context

def get_product_context(request,*args, **kwargs):
    product=ProductRepo(request=request).product(*args, **kwargs)
    if product is None:
        mv=MessageView(request=request)
        mv.title="چنین کالایی یافت نشد."
        return mv.response()
    context=get_product_or_service_context(request=request,item=product,*args, **kwargs)
    product_specifications=product.productspecification_set.all()
    product_specifications_s=json.dumps(ProductSpecificationSerializer(product_specifications,many=True).data)
    context['product_specifications_s']=product_specifications_s
    context['product_specifications']=product_specifications
    if request.user.has_perm(APP_NAME+".add_productspecification"):
        context['add_product_specification_form']=AddProductSpecificationForm()
    
    


    if app_is_installed('guarantee'):
        from guarantee.repo import GuaranteeRepo
        from guarantee.serializers import GuaranteeSerializer
        guarantees=GuaranteeRepo(request=request).list(product_id=product.id)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s

    
    #warehouse availables , warehouse sheets
    warehouse_app_is_installed= app_is_installed('warehouse')
    if warehouse_app_is_installed:
        from warehouse.repo import WareHouseSheetRepo,WareHouseRepo
        from warehouse.serializers import WareHouseSerializer,WareHouseSheetSerializer
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


def get_add_bank_account_context(request,*args, **kwargs):
    context={}
    profiles=ProfileRepo(request=request).list()
    context['profiles']=profiles
    profiles_s=json.dumps(ProfileSerializer(profiles,many=True).data)
    context['profiles_s']=profiles_s
    banks=BankRepo(request=request).list()
    context['banks']=banks
    return context

def getInvoiceLineContext(request,*args, **kwargs):
    context={}
    invoice_line=InvoiceLineRepo(request=request).invoice_line(*args, **kwargs)
    context['invoice_line']=invoice_line
    
    if app_is_installed('guarantee'):
        from guarantee.repo import GuaranteeRepo
        from guarantee.serializers import GuaranteeSerializer
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

    return context
 
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)


class ReportView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['accounts']=accounts
        context['accounts_s']=json.dumps(AccountSerializer(accounts,many=True).data)
        
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)

        context['transaction_statuses']=(u[0] for u in TransactionStatusEnum.choices)
        context['financial_documents_s']='[]'
        context['transactions_s']='[]'
        context['transactions_s']='[]'
        context['get_report_form']=GetReportForm()
        return render(request,TEMPLATE_ROOT+"report.html",context)
    def post(self,request,*args, **kwargs):
        return apis.GetReportApi().post(request=request,*args, **kwargs)


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


            products=ProductRepo(request=request).list(search_for=search_for)
            context['products']=products
            context['products_s']=json.dumps(ProductSerializer(products,many=True).data)



            services=ServiceRepo(request=request).list(search_for=search_for)
            context['services']=services
            context['services_s']=json.dumps(ServiceSerializer(services,many=True).data)

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
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="فاکتور پیدا نشد."
            mv.body="فاکتور پیدا نشد."
            return mv.response()
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,invoice_line in enumerate(invoice.invoice_lines(),start=1):
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
        report_work_book=ReportWorkBook(origin_file_name=f'Invoice.xlsx')
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
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=None,
            style=style,
            sheet_name='Invoice',
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
        invoice,result,message=InvoiceRepo(request=request).create_invoice(*args, **kwargs)
        if invoice is not None:
            url=reverse(APP_NAME+":edit_invoice",kwargs={'pk':invoice.pk})
            return redirect(url)
        else:
            back_url=reverse(APP_NAME+":home")
            back_url=request.META.get('HTTP_REFERER')
            mv=MessageView(request=request)
            mv.title=message
            mv.body=message
            mv.message=message
            mv.back_url=back_url
            return mv.response()


class InvoiceLetterOfIntentView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="فاکتور پیدا نشد."
            mv.body="فاکتور پیدا نشد."
            return mv.response()
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,invoice_line in enumerate(invoice.invoice_lines(),1):
            line={
                'ردیف':i,
                'title':invoice_line.product_or_service.title,
                'آدرس':invoice_line.quantity,      
                'unit_name':invoice_line.unit_name,      
                'unit_price':0,      
                'line_total':0,      
            }
            lines.append(line)
               
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'Invoice.xlsx')
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
            sheet_name='Invoice',
        ) 
        file_name=f"""{date.replace('/','').replace(':','')}   Page {1}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

 
class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        
        context['COEF_PRICE']=1
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="چنین فاکتوری یافت نشد."
            return mv.response()
        context.update(get_invoice_context(request=request,*args, **kwargs))
        # context['no_navbar']=True
        # context['no_footer']=True

    
        if request.user.has_perm('warehouse.add_warehousesheet'):
            from warehouse.enums import WareHouseSheetDirectionEnum
            from warehouse.repo import WareHouseSheetRepo,WareHouseRepo
            from warehouse.forms import AddWarehouseSheetForm,AddWarehouseSheetsForInvoiceForm
            context['add_ware_house_sheet_form']=AddWarehouseSheetsForInvoiceForm()
            ware_houses=WareHouseRepo(request=request).list()
            context['directions']=(direction[0] for direction in WareHouseSheetDirectionEnum.choices)
            context['ware_houses']=ware_houses
            
        return render(request,TEMPLATE_ROOT+"invoice.html",context)

class InvoicePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))
        currency=CURRENCY
        context['TRANSACTION_PRINTING']=True
        context['TUMAN']=True
        context['RIAL']=False
        context['COEF_PRICE']=1
        if 'currency' in kwargs:
            currency=kwargs['currency']
            if currency=='r':
                context['TUMAN']=False
                context['RIAL']=True
                from core.constants import RIAL
                context['CURRENCY']=RIAL
                if CURRENCY==TUMAN:
                    context['COEF_PRICE']=10
        context['no_footer']=True
        context['no_navbar']=True
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)
class InvoiceOfficialPrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_invoice_context(request=request,*args, **kwargs))

        context['COEF_PRICE']=10
        context['TUMAN']=False
        context['RIAL']=True
        from core.constants import RIAL
        context['CURRENCY']=RIAL

        context['no_footer']=True
        context['no_navbar']=True
        return render(request,TEMPLATE_ROOT+"invoice-official-print.html",context)
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
        context.update(getInvoiceLineContext(request=request,*args, **kwargs))
        invoice_line=InvoiceLineRepo(request=request).invoice_line(*args, **kwargs)
        context['invoice_line']=invoice_line

            
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
        if 'account_id_1' in kwargs:
            context['account_id_1']=kwargs['account_id_1']
        if 'account_id_2' in kwargs:
            context['account_id_2']=kwargs['account_id_2']
        if 'account_id' in kwargs:
            context['account_id']=kwargs['account_id']
        transactions=TransactionRepo(request=request).list(*args, **kwargs).order_by('-transaction_datetime')
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        context['expand_transactions']=True
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
class TransactionsExcelView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s


        now=PersianCalendar().date
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,transaction in enumerate(transactions,1):
            line={
                'ردیف':i,
                'عنوان':transaction.title,
                'پرداخت کننده':transaction.pay_from.title,      
                'دریافت کننده':transaction.pay_to.title,      
                'مبلغ':transaction.amount,      
                'تاریخ':PersianCalendar().from_gregorian(transaction.transaction_datetime),      
            }
            lines.append(line) 
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'Page.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
 
        report_work_book.add_sheet(
             data=lines,
            start_row=3,
            start_col=1,
            table_has_header=False,
            table_headers=None,
            style=style,
            sheet_name='links',
        )
      
        file_name=f"""{date.replace('/','').replace(':','')}   Page {1}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response
        
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

 
class CategoriesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        categories=CategoryRepo(request=request).list(parent_id=0,*args, **kwargs)
        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s
        context['expand_categories']=True
        if request.user.has_perm(APP_NAME+".add_category"):
            context['add_category_form']=AddCategoryForm()
        return render(request,TEMPLATE_ROOT+"categories.html",context)


class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['expand_categories']=True
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args, **kwargs)
        if category is None:
            mv=MessageView(request=request)
            mv.title="دسته بندی مورد نظر یافت نشد."
        # context['expand_products']=True
        # context['expand_services']=True
        products_or_services=category.products_or_services.all()

        products=products_or_services.filter(class_name='product')
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        

        services=products_or_services.filter(class_name='service')
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s



        context['category']=category
        categories=category_repo.list(parent_id=category.id)
        context['categories']=categories
        context['categories_s']=json.dumps(CategorySerializer(categories,many=True).data)

        if request.user.has_perm(APP_NAME+".add_category"):
            context['add_category_form']=AddCategoryForm()


        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form']=AddProductForm()
            context['unit_names']=(i[0] for i in UnitNameEnum.choices)
        return render(request,TEMPLATE_ROOT+"category.html",context)


class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        context['expand_products']=True
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        context.update(add_product_context(request=request))
        return render(request,TEMPLATE_ROOT+"products.html",context)

class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        if product is None:
            mv=MessageView(request=request)
            mv.title="چنین کالایی یافت نشد."
        context.update(get_product_context(request=request,product=product))
        return render(request,TEMPLATE_ROOT+"product.html",context)

class BankAccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bank_accounts=BankAccountRepo(request=request).list()
        context['bank_accounts']=bank_accounts
        context['expand_bank_accounts']=True
        bank_accounts_s=json.dumps(BankAccountSerializer(bank_accounts,many=True).data)
        context['bank_accounts_s']=bank_accounts_s
        context.update(get_add_bank_account_context(request=request))
        return render(request,TEMPLATE_ROOT+"bank-accounts.html",context)

class BankAccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bank_account=BankAccountRepo(request=request).bank_account(*args, **kwargs)
        context['bank_account']=bank_account
        if bank_account is None:
            mv=MessageView(request=request)
            mv.title="چنین حسابی یافت نشد."
        context.update(get_account_context(request=request,account=bank_account))
        return render(request,TEMPLATE_ROOT+"bank-account.html",context)



class DoubleTransactionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        # double_transaction=DoubleTransactionRepo(request=request).double_transaction(*args, **kwargs)
        # context['double_transaction']=double_transaction
        context.update(get_double_transaction_context(request=request,*args, **kwargs))
        if context['double_transaction'] is None:
            mv=MessageView(request=request)
            mv.title="چنین تراکنشی یافت نشد."
        return render(request,TEMPLATE_ROOT+"double-transaction.html",context)

class DoubleTransactionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if 'account_id_1' in kwargs:
            context['account_id_1']=kwargs['account_id_1']
        if 'account_id_2' in kwargs:
            context['account_id_2']=kwargs['account_id_2']
        if 'account_id' in kwargs:
            context['account_id']=kwargs['account_id']
        transactions=TransactionRepo(request=request).list(*args, **kwargs).order_by('-transaction_datetime')
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        context['expand_transactions']=True
        return render(request,TEMPLATE_ROOT+"transactions.html",context)


class BanksView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        banks=BankRepo(request=request).list()
        context['banks']=banks
        context['expand_banks']=True
        banks_s=json.dumps(BankSerializer(banks,many=True).data)
        context['banks_s']=banks_s
        return render(request,TEMPLATE_ROOT+"banks.html",context)

class BankView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        bank=BankRepo(request=request).bank(*args, **kwargs)
        context['bank']=bank
        if bank is None:
            mv=MessageView(request=request)
            mv.title="چنین بانکی یافت نشد."
        return render(request,TEMPLATE_ROOT+"bank.html",context)



class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        context['expand_services']=True
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
            context.update(add_transaction_context(request=request))
            context['add_cheque_form']=AddChequeForm()
            context['banks']=BankRepo(request=request).list()
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
        me_account=context['me_account']
        if account==me_account:
            context['account_is_me']=True
        context.update(get_account_context(request=request,account=account))
        return render(request,TEMPLATE_ROOT+"account.html",context)      
class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts=AccountRepo(request=request).list(*args, **kwargs)
        context['accounts']=accounts
        accounts_s=json.dumps(AccountSerializerFull(accounts,many=True).data)
        context['accounts_s']=accounts_s
        context['expand_accounts']=True
        if request.user.has_perm(APP_NAME+".add_account"):
            context['add_account_form']=AddAccountForm()
        return render(request,TEMPLATE_ROOT+"accounts.html",context)

     

class PaymentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        payments=PaymentRepo(request=request).list(*args, **kwargs).order_by('-transaction_datetime')
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


class CostsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        costs=CostRepo(request=request).list(*args, **kwargs)
        context['costs']=costs
        context['expand_costs']=True

        context['costs_s']=json.dumps(CostSerializer(costs,many=True).data)
        if request.user.has_perm(APP_NAME+".add_cost"):
            context.update(get_add_cost_context(request=request))
        return render(request,TEMPLATE_ROOT+"costs.html",context)
class CostView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        cost=CostRepo(request=request).cost(*args, **kwargs)
        context['payment_s']=json.dumps(CostSerializer(cost).data)
        context['cost']=cost
        context.update(get_transaction_context(request=request,transaction=cost))
        return render(request,TEMPLATE_ROOT+"cost.html",context)

class FinancialDocumentsView(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED
        }
        SearchForm_=SearchForm(request.POST)
        if SearchForm_.is_valid():
            cd=SearchForm_.cleaned_data
            cd['start_date']=PersianCalendar().to_gregorian(cd['start_date'])
            cd['end_date']=PersianCalendar().to_gregorian(cd['end_date'])
            financial_documents=FinancialDocumentRepo(request=request).list(**cd)
            context['financial_documents']=FinancialDocumentSerializer(financial_documents,many=True).data
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
        if financial_document is None:
            mv=MessageView(request=request)
            mv.title="چنین سندی یافت نشد."
            mv.body="چنین سندی یافت نشد."
            return mv.response()
        financial_document.normalize_balances()

        context['financial_document']=financial_document
        financial_balances=FinancialBalanceRepo(request=request).list(financial_document_id=financial_document.id)
        context['financial_balances']=financial_balances

        transactions=[financial_document.transaction]
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s


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
