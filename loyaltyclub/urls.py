from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.IndexView.as_view(),name="home"),
    path('customers/',views.CustomersView.as_view(),name="customers"),
    path('customer/<int:pk>/',views.CustomerView.as_view(),name="customer"),
    path('orders/',views.OrdersView.as_view(),name="orders"),
    path('order/<int:pk>/',views.OrderView.as_view(),name="order"),
    path('add_order/',apis.AddOrderView.as_view(),name="add_order"),
]
