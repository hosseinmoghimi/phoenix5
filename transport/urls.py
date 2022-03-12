from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("drivers/",views.DriversView.as_view(),name="drivers"),
    path("driver/<int:pk>/",views.DriverView.as_view(),name="driver"),
    path("trippath/<int:pk>/",views.TripPathView.as_view(),name="trippath"),

    
    path("passengers/",views.PassengersView.as_view(),name="passengers"),
    path("passenger/<int:pk>/",views.PassengerView.as_view(),name="passenger"),


]
