from .apps import APP_NAME
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("search/",(views.SearchView.as_view()),name="search"),
    path("product/<int:pk>/",login_required(views.HomeView.as_view()),name="product"),
    path("brands/",login_required(views.HomeView.as_view()),name="brands"),
    path("category/<int:pk>/",login_required(views.HomeView.as_view()),name="category"),
    path("product/<int:pk>/",login_required(views.HomeView.as_view()),name="product"),
    path("ware_houses/",login_required(views.HomeView.as_view()),name="ware_houses"),
    path("suppliers/",login_required(views.HomeView.as_view()),name="suppliers"),
]
