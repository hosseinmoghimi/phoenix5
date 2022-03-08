from .apps import APP_NAME
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.HomeView.as_view()),name="search"),
    path("service/<int:pk>/",login_required(views.ServiceViews.as_view()),name="service"),
    path("services/",login_required(views.ServicesViews.as_view()),name="services"),
    path("product/<int:pk>/",login_required(views.ProductViews.as_view()),name="product"),
    path("products/",login_required(views.ProductsViews.as_view()),name="products"),
]
