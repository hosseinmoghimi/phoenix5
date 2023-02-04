from django.urls import path
from organization.apps import APP_NAME
from organization import views,apis
from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name="home"),
    
    path("employee/<int:pk>/",login_required(views.EmployeeView.as_view()),name="employee"),
    path("employees/",login_required(views.EmployeesView.as_view()),name="employees"),
    path("add_employee/",login_required(apis.AddEmployeeApi.as_view()),name="add_employee"),
    
    
    path("organization_units/",login_required(views.OrganizationUnitsView.as_view()),name="organization_units"),
    path("organization_unit/<int:pk>/",login_required(views.OrganizationUnitView.as_view()),name="organizationunit"),
    path("org_chart/<int:pk>/",login_required(views.OrganizationUnitChartView.as_view()),name="org_chart"),
    path('add_organization_unit/',login_required(apis.AddOrganizationUnitApi.as_view()),name="add_organization_unit"),

    path('select_organization_unit/',login_required(apis.SelectOrganizationUnitApi.as_view()),name="select_organization_unit"),


    path("letters/",login_required(views.LettersView.as_view()),name="letters"),
    path("add_letter/",login_required(views.AddLetterView.as_view()),name="add_letter"),
    path("send_letter/",login_required(apis.SendLetterApi.as_view()),name="send_letter"),
    path("letter/<int:pk>/",login_required(views.LetterView.as_view()),name="letter"),
    path("letter_print/<int:pk>/",login_required(views.LetterPrintView.as_view()),name="letter_print"),

]
