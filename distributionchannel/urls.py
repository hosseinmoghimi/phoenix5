from django.urls import path
from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name='home'),
]
