from warehouse.apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.HomeView.as_view(),name='home,'),
    path('ware_house/<int:pk>/',login_required(views.WareHouseViews.as_view()),name="warehouse"),
    path('ware_houses/',login_required(views.WareHousesViews.as_view()),name="ware_houses"),
    path('ware_house_print/<int:pk>/',login_required(views.WareHousePrintViews.as_view()),name="ware_house_print"),
    path('ware_house_sheet_signature/<int:pk>/',login_required(views.WareHousePrintViews.as_view()),name="warehousesheetsignature"),
    path('ware_house_sheet/<int:pk>/',login_required(views.WareHouseSheetViews.as_view()),name="warehousesheet"),
    # path('profile_financial_account/<pk>/',login_required(views.ReportViews().profile_financial_account),name="profile_financial_account"),
    path('change_warehouse_sheet_state/',login_required(apis.WareHouseSheetApi.as_view()),name="change_warehouse_sheet_state"),
    path('report/',login_required(apis.ReportApi.as_view()),name="report"),
    path('add_signature/',login_required(apis.AddSignatureApi.as_view()),name="add_signature"),
    path('add_warehouse/',login_required(apis.AddWareHouseApi.as_view()),name="add_warehouse"),
    path('add_warehouse_sheet/',login_required(apis.AddWareHouseSheetApi.as_view()),name="add_warehouse_sheet"),
    path('add_warehouse_sheets_for_invoice/',login_required(apis.AddWareHouseSheetsForInvoiceApi.as_view()),name="add_warehouse_sheets_for_invoice"),
    

]
