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
    path("trip_paths/",views.TripPathsView.as_view(),name="trip_paths"),
    path("trip/<int:pk>/",views.TripView.as_view(),name="trip"),
    path("trips/",views.TripsView.as_view(),name="trips"),

    path("vehicle/<int:pk>/",views.TripView.as_view(),name="vehicle"),
    path("vehicles/",views.TripsView.as_view(),name="vehicles"),

    path("tripcategory/<int:pk>/",views.TripView.as_view(),name="tripcategory"),
    path("tripcategories/",views.TripsView.as_view(),name="tripcategories"),
    
    path("passengers/",views.PassengersView.as_view(),name="passengers"),
    path("passenger/<int:pk>/",views.PassengerView.as_view(),name="passenger"),


]
