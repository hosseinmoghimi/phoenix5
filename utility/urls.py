from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("charts/",(views.ChartsView.as_view()),name="charts"),
    

]
