from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("add_trip_path/",views.AddTripPathView.as_view(),name="add_trip_path"),
    path("add_trip/",views.AddTripView.as_view(),name="add_trip"),

    path("drivers/",views.DriversView.as_view(),name="drivers"),
    path("driver/<int:pk>/",views.DriverView.as_view(),name="driver"),
    path("add_driver/",apis.AddDriverApi.as_view(),name="add_driver"),

    path("trip_categories/",views.TripCategoriesView.as_view(),name="trip_categories"),
    path("trip_category/<int:pk>/",views.TripCategoryView.as_view(),name="tripcategory"),
    path("add_trip_category/",apis.AddTripCategoryApi.as_view(),name="add_trip_category"),


    path("trippath/<int:pk>/",views.TripPathView.as_view(),name="trippath"),
    path("trip_paths/",views.TripPathsView.as_view(),name="trip_paths"),
    path("add_trippath/",apis.AddTripPathApi.as_view(),name="add_trippath"),

    
    path("trip/<int:pk>/",views.TripView.as_view(),name="trip"),
    path("trips/",views.TripsView.as_view(),name="trips"),


    
    path("service_man/<int:pk>/",views.ServiceManView.as_view(),name="serviceman"),
    path("service_mans/",views.ServiceMansView.as_view(),name="servicemans"),
    path("add_service_man/",apis.AddServiceManApi.as_view(),name="add_service_man"),
    
    path("maintenance/<int:pk>/",views.MaintenanceView.as_view(),name="maintenance"),
    path("maintenances/",views.MaintenancesView.as_view(),name="maintenances"),
    path("add_maintenance/",apis.AddMaintenanceApi.as_view(),name="add_maintenance"),
    
    path("work_shift/<int:pk>/",views.WorkShiftView.as_view(),name="workshift"),
    path("work_shifts/",views.WorkShiftsView.as_view(),name="workshifts"),
    path("add_work_shift/",login_required(apis.AddWorkShiftApi.as_view()),name="add_work_shift"),

    path("vehicle/<int:pk>/",views.VehicleView.as_view(),name="vehicle"),
    path("vehicles/",views.VehiclesView.as_view(),name="vehicles"),
    path("add_vehicle/",apis.AddVehicleApi.as_view(),name="add_vehicle"),

    path("client/<int:pk>/",views.ClientView.as_view(),name="client"),
    path("clients/",views.ClientsView.as_view(),name="clients"),
    path("add_client/",apis.AddClientApi.as_view(),name="add_client"),
 
    
    path("passengers/",views.PassengersView.as_view(),name="passengers"),
    path("passenger/<int:pk>/",views.PassengerView.as_view(),name="passenger"),
    path("add_passenger/",apis.AddPassengerApi.as_view(),name="add_passenger"),


]
