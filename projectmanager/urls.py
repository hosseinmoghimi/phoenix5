from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.HomeView.as_view(),name="search"),
    path("material_invoice/<int:pk>/",login_required(views.HomeView.as_view()),name="materialinvoice"),
    path("service_invoice/<int:pk>/",login_required(views.HomeView.as_view()),name="serviceinvoice"),

    path("materials/",login_required(views.MaterialsView.as_view()),name="materials"),
    path("material/<int:pk>/",login_required(views.MaterialView.as_view()),name="material"),

    path("service/<int:pk>/",login_required(views.ServiceView.as_view()),name="pm_service"),
    path("services/",login_required(views.ServicesView.as_view()),name="services"),

]
