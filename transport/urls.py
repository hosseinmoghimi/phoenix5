from .apps import APP_NAME
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"),
    path("search/",login_required(views.SearchView.as_view()),name="search"),
    path("add_trip_path/",login_required(views.AddTripPathView.as_view()),name="add_trip_path"),
    path("add_trip/",login_required(views.AddTripView.as_view()),name="add_trip"),

    path("drivers/",login_required(views.DriversView.as_view()),name="drivers"),
    path("driver/<int:pk>/",login_required(views.DriverView.as_view()),name="driver"),
    path("add_driver/",login_required(apis.AddDriverApi.as_view()),name="add_driver"),

    path("trip_categories/",login_required(views.TripCategoriesView.as_view()),name="trip_categories"),
    path("trip_category/<int:pk>/",login_required(views.TripCategoryView.as_view()),name="tripcategory"),
    path("add_trip_category/",login_required(apis.AddTripCategoryApi.as_view()),name="add_trip_category"),

    path("luggage/<int:pk>/",login_required(views.LuggageView.as_view()),name="luggage"),
    path("luggages/",login_required(views.LuggagesView.as_view()),name="luggages"),
    path("add_luggage/",login_required(apis.AddLuggageApi.as_view()),name="add_luggage"),

    

    path("trippath/<int:pk>/",login_required(views.TripPathView.as_view()),name="trippath"),
    path("trip_paths/",login_required(views.TripPathsView.as_view()),name="trip_paths"),
    path("add_trippath/",login_required(apis.AddTripPathApi.as_view()),name="add_trippath"),

    
    path("trip/<int:pk>/",login_required(views.TripView.as_view()),name="trip"),
    path("trips/",login_required(views.TripsView.as_view()),name="trips"),


    
    path("service_man/<int:pk>/",login_required(views.ServiceManView.as_view()),name="serviceman"),
    path("service_mans/",login_required(views.ServiceMansView.as_view()),name="servicemans"),
    path("add_service_man/",login_required(apis.AddServiceManApi.as_view()),name="add_service_man"),
    
    path("maintenance/<int:pk>/",login_required(views.MaintenanceView.as_view()),name="maintenance"),
    path("maintenances/",login_required(views.MaintenancesView.as_view()),name="maintenances"),
    path("add_maintenance/",login_required(apis.AddMaintenanceApi.as_view()),name="add_maintenance"),
    
    path("work_shift/<int:pk>/",login_required(views.WorkShiftView.as_view()),name="workshift"),
    path("work_shifts/",login_required(views.WorkShiftsView.as_view()),name="workshifts"),
    path("add_work_shift/",login_required(apis.AddWorkShiftApi.as_view()),name="add_work_shift"),

    path("vehicle/<int:pk>/",login_required(views.VehicleView.as_view()),name="vehicle"),
    path("vehicles/",login_required(views.VehiclesView.as_view()),name="vehicles"),
    path("add_vehicle/",login_required(apis.AddVehicleApi.as_view()),name="add_vehicle"),

    path("client/<int:pk>/",login_required(views.ClientView.as_view()),name="client"),
    path("clients/",login_required(views.ClientsView.as_view()),name="clients"),
    path("add_client/",login_required(apis.AddClientApi.as_view()),name="add_client"),
 
    
    path("passengers/",login_required(views.PassengersView.as_view()),name="passengers"),
    path("passenger/<int:pk>/",login_required(views.PassengerView.as_view()),name="passenger"),
    path("add_passenger/",login_required(apis.AddPassengerApi.as_view()),name="add_passenger"),


]
