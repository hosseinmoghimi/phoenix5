from django.urls import path
from .apps import APP_NAME
from . import views
urlpatterns = [
    path("",views.HomeView.as_view(),name="view"),
]
