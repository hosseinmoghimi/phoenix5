from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.HomeView.as_view(),name="search"),

    path("projects/",login_required(views.ProjectsView.as_view()),name="projects"),
    path("project/<int:pk>/",login_required(views.ProjectView.as_view()),name="project"),

    path("organization_units/",login_required(views.OrganizationUnitsView.as_view()),name="organization_units"),
    path("organization_unit/<int:pk>/",login_required(views.OrganizationUnitView.as_view()),name="organizationunit"),


    path("material_invoice/<int:pk>/",login_required(views.HomeView.as_view()),name="materialinvoice"),
    path("service_invoice/<int:pk>/",login_required(views.HomeView.as_view()),name="serviceinvoice"),

    path("materials/",login_required(views.MaterialsView.as_view()),name="materials"),
    path("material/<int:pk>/",login_required(views.MaterialView.as_view()),name="material"),

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="pm_service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),


    path('add_organization_unit/',login_required(apis.AddOrganizationUnitApi.as_view()),name="add_organization_unit"),

]
