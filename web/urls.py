from .apps import APP_NAME
from django.urls import path
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.HomeView.as_view(),name="search"),
    path("add_blog/",views.HomeView.as_view(),name="add_blog"),
]
