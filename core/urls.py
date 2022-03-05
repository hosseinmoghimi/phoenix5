
from . import views,apis
from .apps import APP_NAME
from django.urls import path

app_name=APP_NAME
urlpatterns = [
    path('change_parameter/',apis.ChangeParameterApi.as_view(),name="change_parameter")
]
