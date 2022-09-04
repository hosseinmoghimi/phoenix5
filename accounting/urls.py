from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.SearchView.as_view()),name="search"),
    path("report/",login_required(views.ReportView.as_view()),name="report"),
    path("search_json/",login_required(views.SearchJsonView.as_view()),name="search_json"),

    path("bank_accounts/",login_required(views.BankAccountsView.as_view()),name="bank_accounts"),
    path("bank_account/<int:pk>/",login_required(views.BankAccountView.as_view()),name="bankaccount"),
    path("add_bank_account/",login_required(apis.AddBankAccountApi.as_view()),name="add_bank_account"),

    path("bank/",login_required(views.BanksView.as_view()),name="banks"),
    path("bank/<int:pk>/",login_required(views.BankView.as_view()),name="bank"),
    path("add_bank/",login_required(apis.AddBankApi.as_view()),name="add_bank"),

    path("products/",login_required(views.ProductsView.as_view()),name="products"),
    path("product/<int:pk>/",(views.ProductView.as_view()),name="product"),

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),


    path("cheque/<int:pk>/",login_required(views.ChequeView.as_view()),name="cheque"),
    path("cheques/",login_required(views.ChequesView.as_view()),name="cheques"), 
    
    path("transaction/<int:pk>/",login_required(views.TransactionView.as_view()),name="transaction"),
    path("transactions/<int:account_id>/",login_required(views.TransactionsView.as_view()),name="account_transactions"),
    path("transactions/",login_required(views.TransactionsView.as_view()),name="transactions"),
    path("transactions/<int:account_id>/",login_required(views.TransactionsView.as_view()),name="transactions1"),
    path("transactions/<int:account_id_1>/<int:account_id_2>/",login_required(views.TransactionsView.as_view()),name="transactions2"),
    path("transactions_excel/<int:account_id>/",login_required(views.TransactionsExcelView.as_view()),name="transactions1_excel"),
    path("transactions_excel/<int:account_id_1>/<int:account_id_2>/",login_required(views.TransactionsExcelView.as_view()),name="transactions2_excel"),
    path("transactions_print/",login_required(views.TransactionsPrintView.as_view()),name="transactions_print"),
    
    path("product_or_service_category/<int:pk>/",login_required(views.ProductOrServiceCategoryView.as_view()),name="product_or_service_category"),
    path("product_or_service_categories/",login_required(views.ProductOrServiceCategoriesView.as_view()),name="product_or_service_categories"),
    
    path("category/<int:pk>/",login_required(views.CategoryView.as_view()),name="category"),
    path("categories/",login_required(views.CategoriesView.as_view()),name="categories"),
    
    path("account/<int:pk>/",login_required(views.AccountView.as_view()),name="account"),
    path("accounts/",login_required(views.AccountsView.as_view()),name="accounts"),
    path("add_account/",login_required(apis.AddAccountApi.as_view()),name="add_account"),

    path("invoice_line/<int:pk>/",login_required(views.InvoiceLineView.as_view()),name="invoiceline"),
    path("invoice/edit/<int:pk>/",login_required(views.InvoiceEditView.as_view()),name="edit_invoice"),
    path("invoices/<int:account_id>/",login_required(views.InvoicesView.as_view()),name="account_invoices"),
    path("invoices/",login_required(views.InvoicesView.as_view()),name="invoices"),
    path("invoice/excel/<int:pk>/",login_required(views.InvoiceExcelView.as_view()),name="invoice_excel"),
    path("invoice/<int:pk>/",login_required(views.InvoiceView.as_view()),name="invoice"),
    path("invoice/print/<int:pk>/",login_required(views.InvoicePrintView.as_view()),name="invoice_print"),
    path("invoice/official_print/<int:pk>/",login_required(views.InvoiceOfficialPrintView.as_view()),name="invoice_official_print"),
    path("invoice/invoice_letter_of_intent/<int:pk>/",login_required(views.InvoiceLetterOfIntentView.as_view()),name="invoice_letter_of_intent"),
    path("new_invoice/<int:pay_from_id>/<int:pay_to_id>/",login_required(views.NewInvoiceView.as_view()),name="new_invoice"),
    path("invoice/print/<int:pk>/<currency>/",login_required(views.InvoicePrintView.as_view()),name="invoice_print_currency"),

    path("financial_document/<int:pk>/",login_required(views.FinancialDocumentView.as_view()),name="financialdocument"),
    path("financial_documents/",login_required(views.FinancialDocumentsView.as_view()),name="financial_documents"),
    path("financial_documents/<int:account_id>/",login_required(views.FinancialDocumentsView.as_view()),name="account_financial_documents"),
    
    path("asset/<int:pk>/",login_required(views.AssetView.as_view()),name="asset"),
    path("assets/",login_required(views.AssetsView.as_view()),name="assets"),
    
    path("financial_balance/<int:pk>/",login_required(views.FinancialBalanceView.as_view()),name="financialbalance"),
    path("financial_balances/",login_required(views.FinancialBalancesView.as_view()),name="financial_balances"),
    path("add_financial_balance/",login_required(apis.AddFinancialBalancesApi.as_view()),name="add_financial_balance"),
    
    path("payment/<int:pk>/",login_required(views.PaymentView.as_view()),name="payment"),
    path("payments/",login_required(views.PaymentsView.as_view()),name="payments"),
    
    path("cost/<int:pk>/",login_required(views.CostView.as_view()),name="cost"),
    path("costs/",login_required(views.CostsView.as_view()),name="costs"),
    path("add_cost/",login_required(apis.AddCostApi.as_view()),name="add_cost"),
    



  path("add_payment/",login_required(apis.AddPaymentApi.as_view()),name="add_payment"),
  path("add_cheque/",login_required(apis.AddChequeApi.as_view()),name="add_cheque"),
  path("add_price/",login_required(apis.AddPriceApi.as_view()),name="add_price"),

  
  path('change_product_or_service_category/',login_required(apis.ChangeProductOrServiceCategoryApi.as_view()),name="change_product_or_service_category"),

  path("add_category/",login_required(apis.AddCategoryApi.as_view()),name="add_category"),
  path('add_item_category/',login_required(apis.AddItemCategoryApi.as_view()),name="add_item_category"),
  path('add_product_or_service_category/',login_required(apis.AddProductOrServiceCategoryApi.as_view()),name="add_product_or_service_category"),
  path('add_product/',login_required(apis.AddProductApi.as_view()),name="add_product"),
  path('add_service/',login_required(apis.AddServiceApi.as_view()),name="add_service"),
  path('print_transaction/',login_required(apis.PrintTransactionApi.as_view()),name="print_transaction"),
  path('roll_back_transaction/',login_required(apis.RollBackTransactionApi.as_view()),name="roll_back_transaction"),



]
