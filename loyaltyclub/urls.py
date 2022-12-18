from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.IndexView.as_view(),name="home"),

    path('customers/',views.CustomersView.as_view(),name="customers"),
    path('customer/<int:pk>/',views.CustomerView.as_view(),name="customer"),

    path('suppliers/',views.SuppliersView.as_view(),name="suppliers"),
    path('supplier/<int:pk>/',views.SupplierView.as_view(),name="supplier"),
    
    path('coefs/',views.CoefsView.as_view(),name="coefs"),
    path('change_coef/',apis.ChangeCoefView.as_view(),name="change_coef"),

    path('coupons/',views.CouponsView.as_view(),name="coupons"),
    path('coupon/<int:pk>/',views.CouponView.as_view(),name="coupon"),

    path('orders/',views.OrdersView.as_view(),name="orders"),
    path('order/<int:pk>/',views.OrderView.as_view(),name="order"),
    path('add_order/',apis.AddOrderView.as_view(),name="add_order"),

]
