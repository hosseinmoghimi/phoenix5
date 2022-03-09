from .apps import APP_NAME
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.HomeView.as_view()),name="search"),
    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),
    path("account/<int:pk>/",login_required(views.AccountView.as_view()),name="account"),
    path("financial_accounts/",login_required(views.AccountsView.as_view()),name="accounts"),
    path("product/<int:pk>/",login_required(views.ProductView.as_view()),name="product"),
    path("products/",login_required(views.ProductsView.as_view()),name="products"),
    path("financial_document/<int:pk>/",login_required(views.FinancialDocumentView.as_view()),name="financialdocument"),
    path("financial_documents/",login_required(views.FinancialDocumentsView.as_view()),name="financial_documents"),

]
