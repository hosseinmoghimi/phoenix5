from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('location/<int:pk>/',views.LocationView.as_view(),name='location'),
    path('locations/',views.LocationsView.as_view(),name='locations'),
    path('add_location/',apis.AddLocationApi.as_view(),name='add_location'),
    path('add_page_location/',apis.AddPageLocationApi.as_view(),name='add_page_location'),
]
