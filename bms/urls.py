from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from bms.apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name='home'),
    
]
