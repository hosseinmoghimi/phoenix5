from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('location/<int:pk>/',views.LocationView.as_view(),name='location'),
    path('locations/',views.LocationsView.as_view(),name='locations'),
    path('areas/',views.AreasView.as_view(),name='areas'),
    path('area/<int:pk>/',views.AreaView.as_view(),name='area'),
    path('add_location/',apis.AddLocationApi.as_view(),name='add_location'),
    path('add_page_location/',apis.AddPageLocationApi.as_view(),name='add_page_location'),
    path('add_area/',apis.AddAreaApi.as_view(),name='add_area'),
]
