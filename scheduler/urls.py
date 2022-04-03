from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"), 
    path("appointment/<int:pk>/",(views.AppointmentView.as_view()),name="appointment"), 
    path("appointments/",(views.AppointmentsView.as_view()),name="appointments"), 
    path("add_appointment/",(apis.AddAppointmentApi.as_view()),name="add_appointment"), 
]