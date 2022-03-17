from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.HomeView.as_view()),name="search"),

    path("products/",login_required(views.ProductsView.as_view()),name="products"),
    path("product/<int:pk>/",login_required(views.ProductView.as_view()),name="product"),


    path("cheque/<int:pk>/",login_required(views.ChequeView.as_view()),name="cheque"),
    path("cheques/",login_required(views.ChequesView.as_view()),name="cheques"), 

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),
    
    path("transaction/<int:pk>/",login_required(views.TransactionView.as_view()),name="transaction"),
    path("transactions/",login_required(views.TransactionsView.as_view()),name="transactions"),
    
    path("account/<int:pk>/",login_required(views.AccountView.as_view()),name="account"),
    path("financial_accounts/",login_required(views.AccountsView.as_view()),name="accounts"),

    path("edit-invoice/<int:pk>/",login_required(views.EditInvoiceView.as_view()),name="edit_invoice"),
    path("invoices/",login_required(views.InvoicesView.as_view()),name="invoices"),
    path("invoice/<int:pk>/",login_required(views.InvoiceView.as_view()),name="invoice"),

    path("financial_document/<int:pk>/",login_required(views.FinancialDocumentView.as_view()),name="financialdocument"),
    path("financial_documents/",login_required(views.FinancialDocumentsView.as_view()),name="financial_documents"),




  path("add_cheque/",login_required(apis.AddChequeApi.as_view()),name="add_cheque"),


]
