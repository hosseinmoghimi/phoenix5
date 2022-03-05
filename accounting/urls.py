from .apps import APP_NAME
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.HomeView.as_view()),name="search"),
    path("product/<int:pk>/",login_required(views.HomeView.as_view()),name="product"),
]
