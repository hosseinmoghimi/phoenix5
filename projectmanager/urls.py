from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("employee/<int:pk>/",login_required(views.EmployeeView.as_view()),name="employee"),
    path("employees/",login_required(views.EmployeesView.as_view()),name="employees"),
    path("material_request/<int:pk>/",login_required(views.RequestView.as_view()),name="materialrequest"),
    path("service_request/<int:pk>/",login_required(views.RequestView.as_view()),name="servicerequest"),
    path("request/<int:pk>/",login_required(views.ProjectView.as_view()),name="request"),
    
    path("request/<int:pk>/",login_required(views.RequestView.as_view()),name="request"), 

    path("letters/",login_required(views.LettersView.as_view()),name="letters"),
    path("letter/<int:pk>/",login_required(views.LetterView.as_view()),name="letter"),

    path("ware_houses/",login_required(views.ProjectsView.as_view()),name="ware_houses"),
    path("ware_house/<int:pk>/",login_required(views.ProjectView.as_view()),name="ware_house"),

    path("projects/",login_required(views.ProjectsView.as_view()),name="projects"),
    path("project/<int:pk>/",login_required(views.ProjectView.as_view()),name="project"),
    path("project_chart/<int:pk>/",login_required(views.ProjectChartView.as_view()),name="project_chart"),

    path("organization_units/",login_required(views.OrganizationUnitsView.as_view()),name="organization_units"),
    path("organization_unit/<int:pk>/",login_required(views.OrganizationUnitView.as_view()),name="organizationunit"),


    path("material_invoice/<int:pk>/",login_required(views.MaterialInvoiceView.as_view()),name="materialinvoice"),
    path("service_invoice/<int:pk>/",login_required(views.ServiceInvoiceView.as_view()),name="serviceinvoice"),

    path("materials/",login_required(views.MaterialsView.as_view()),name="materials"),
    path("material/<int:pk>/",login_required(views.MaterialView.as_view()),name="material"),

    path("event/<int:pk>/",login_required(views.EventView.as_view()),name="event"),
    path("events/",login_required(views.EventsView.as_view()),name="events"),

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="pm_service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),
    path("guantt_chart/<int:pk>/",login_required(views.GuanttChartView.as_view()),name="guantt_chart"),
  
    path('add_material_request/',login_required(apis.AddMaterialRequestApi.as_view()),name="add_material_request"),
    path('add_service_request/',login_required(apis.AddServiceRequestApi.as_view()),name="add_service_request"),
    path('add_organization_unit/',login_required(apis.AddOrganizationUnitApi.as_view()),name="add_organization_unit"),
    path('add_project/',login_required(apis.AddProjectApi.as_view()),name="add_project"),
    path('edit_project/',login_required(apis.EditProjectApi.as_view()),name="edit_project"),
    path('add_event/',login_required(apis.AddEventApi.as_view()),name="add_event"),
    path('add_signature/',login_required(apis.AddSignatureApi.as_view()),name="add_signature"),
    path('add_material/',login_required(apis.AddMaterialApi.as_view()),name="add_material"),
    path('add_service/',login_required(apis.AddServiceApi.as_view()),name="add_service"), 

]
