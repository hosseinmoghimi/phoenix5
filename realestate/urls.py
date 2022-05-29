from django.urls import path
from realestate.apps import APP_NAME
from realestate import views,apis



from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    
    path("",login_required(views.HomeViews.as_view()),name="home"),
    
    path("search/",login_required(views.SearchView.as_view()),name="search"),


    path("properties/",login_required(views.PropertiesView.as_view()),name="properties"),
    path("property/<int:pk>/",login_required(views.PropertyView.as_view()),name="property"),
    
]
