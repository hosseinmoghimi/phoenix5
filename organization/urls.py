from django.urls import path
from organization.apps import APP_NAME
from organization import views,apis
from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name="home"),
    
    path("employee/<int:pk>/",login_required(views.EmployeeView.as_view()),name="employee"),
    path("employees/",login_required(views.EmployeesView.as_view()),name="employees"),
    
    
    path("organization_units/",login_required(views.OrganizationUnitsView.as_view()),name="organization_units"),
    path("organization_unit/<int:pk>/",login_required(views.OrganizationUnitView.as_view()),name="organizationunit"),
    path('add_organization_unit/',login_required(apis.AddOrganizationUnitApi.as_view()),name="add_organization_unit"),




]
