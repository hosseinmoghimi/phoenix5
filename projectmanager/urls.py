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

]
