from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("search/",(views.SearchView.as_view()),name="search"),

    path("product/<int:pk>/",(views.ProductView.as_view()),name="product"),
    path("category/<int:pk>/",(views.CategoryView.as_view()),name="category"),

    path("brands/",(views.HomeView.as_view()),name="brands"),

    path("category/<int:pk>/",(views.CategoryView.as_view()),name="category"),

    path("ware_houses/",login_required(views.HomeView.as_view()),name="ware_houses"),
    
    path("suppliers/",login_required(views.SuppliersView.as_view()),name="suppliers"),
    path("supplier/<int:pk>/",login_required(views.SupplierView.as_view()),name="supplier"),
    
    path("cart/<int:customer_id>/",(views.CartView.as_view()),name="customer_cart"),
    path("cart/",(views.CartView.as_view()),name="cart"),
    
    path("brands/",(views.BrandsView.as_view()),name="brands"),
    path("brand/<int:pk>/",(views.BrandView.as_view()),name="brand"),
    
    path("shops/",(views.ShopsView.as_view()),name="shops"),
    path("shop/<int:pk>/",(views.ShopView.as_view()),name="shop"),

    
    path("customers/",(views.CustomersView.as_view()),name="customers"),
    path("customer/<int:pk>/",(views.CustomerView.as_view()),name="customer"),

    path("invoices/",login_required(views.InvoicesView.as_view()),name="marketinvoices"),
    path("invoices/<int:supplier_id>/<int:customer_id>/",login_required(views.InvoicesView.as_view()),name="marketinvoices_"),
    path("invoice/<int:pk>/",login_required(views.InvoiceView.as_view()),name="marketinvoice"),

    path("api/categories/",(apis.CategoriesApi.as_view()),name="api_categories"),
    path("api/category/<int:category_id>/",(apis.CategoryApi.as_view()),name="api_category"),
    path("api/products/<int:category_id>/",(apis.ProductsApi.as_view()),name="api_category_products"),
    path("add_category/",(apis.AddCategoryApi.as_view()),name="add_category"),
    path("add_product/",(apis.AddProductApi.as_view()),name="add_product"),
    path("add_to_cart/",(apis.AddToCartApi.as_view()),name="add_to_cart"),
    path("add_shop/",(apis.AddShopApi.as_view()),name="add_shop"),
    path("add_customer/",(apis.AddCustomerApi.as_view()),name="add_customer"),
    path("add_supplier/",(apis.AddSupplierApi.as_view()),name="add_supplier"),
    path("checkout/",(apis.CheckoutApi.as_view()),name="checkout"),
    
]
