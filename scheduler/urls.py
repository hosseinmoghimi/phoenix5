from .apps import APP_NAME
from . import views,apis
from django.urls import path
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeView.as_view()),name="home"), 
    path("appointment/<int:pk>/",login_required(views.AppointmentView.as_view()),name="appointment"), 
    path("appointments/",login_required(views.AppointmentsView.as_view()),name="appointments"), 
    path("add_appointment/",login_required(apis.AddAppointmentApi.as_view()),name="add_appointment"), 
]