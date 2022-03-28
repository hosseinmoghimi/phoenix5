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
    path('ware_house_sheet/<int:pk>/',login_required(views.WareHouseSheetViews.as_view()),name="warehousesheet"),
    # path('profile_financial_account/<pk>/',login_required(views.ReportViews().profile_financial_account),name="profile_financial_account"),
    path('change_warehouse_sheet_state/',login_required(apis.WareHouseSheetApi.as_view()),name="change_warehouse_sheet_state"),

]
