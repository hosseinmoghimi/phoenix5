from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.SearchView.as_view()),name="search"),
    path("material_request/<int:pk>/",login_required(views.RequestView.as_view()),name="materialrequest"),
    path("service_request/<int:pk>/",login_required(views.RequestView.as_view()),name="servicerequest"),
    path("request/<int:pk>/",login_required(views.ProjectView.as_view()),name="request"),
    
    path("request/<int:pk>/",login_required(views.RequestView.as_view()),name="request"), 


    path("ware_houses/",login_required(views.ProjectsView.as_view()),name="ware_houses"),
    path("ware_house/<int:pk>/",login_required(views.ProjectView.as_view()),name="ware_house"),

    path("projects/",login_required(views.ProjectsListView.as_view()),name="projects"),
    path("project/<int:pk>/",login_required(views.ProjectView.as_view()),name="project"),
    path("copy_project/",login_required(views.CopyProjectView.as_view()),name="copy_project"),
    path("project_guantt/<int:pk>/",login_required(views.ProjectGuanttView.as_view()),name="project_guantt"),
    path("project_chart/<int:pk>/",login_required(views.ProjectChartView.as_view()),name="project_chart"),

    path("material_invoice/<int:pk>/",login_required(views.MaterialInvoiceView.as_view()),name="materialinvoice"),
    path("service_invoice/<int:pk>/",login_required(views.ServiceInvoiceView.as_view()),name="serviceinvoice"),

    path("materials/",login_required(views.MaterialsView.as_view()),name="materials"),
    path("material/<int:pk>/",login_required(views.MaterialView.as_view()),name="material"),

    path("event/<int:pk>/",login_required(views.EventView.as_view()),name="event"),
    path("events/",login_required(views.EventsView.as_view()),name="events"),

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),
  
    path('add_material_request/',login_required(apis.AddMaterialRequestApi.as_view()),name="add_material_request"),
    path('add_service_request/',login_required(apis.AddServiceRequestApi.as_view()),name="add_service_request"),
    path('add_project/',login_required(apis.AddProjectApi.as_view()),name="add_project"),
    path('edit_project/',login_required(apis.EditProjectApi.as_view()),name="edit_project"),
    path('add_event/',login_required(apis.AddEventApi.as_view()),name="add_event"),
    path('add_signature/',login_required(apis.AddSignatureApi.as_view()),name="add_signature"),
    path('add_material/',login_required(apis.AddMaterialApi.as_view()),name="add_material"),
    path('add_service/',login_required(apis.AddServiceApi.as_view()),name="add_service"), 
    path('copy_service_requests/',login_required(apis.CopyServiceRequestsApi.as_view()),name="copy_service_requests"), 
    path('copy_material_requests/',login_required(apis.CopyMaterialRequestsApi.as_view()),name="copy_material_requests"), 
    path('copy_service_requests_from_invoice/',login_required(apis.CopyServiceRequestsFromInvoiceApi.as_view()),name="copy_service_requests_from_invoice"), 
    path('copy_material_requests_from_invoice/',login_required(apis.CopyMaterialRequestsFromInvoiceApi.as_view()),name="copy_material_requests_from_invoice"), 

]
