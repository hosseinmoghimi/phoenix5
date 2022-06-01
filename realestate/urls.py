from django.urls import path
from realestate.apps import APP_NAME
from realestate import views,apis



from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    
    # path("",login_required(views.HomeViews.as_view()),name="home"),
    
    path("",login_required(views.PropertiesView.as_view()),name="home"),
    path("search/",login_required(views.SearchView.as_view()),name="search"),


    path("agent/<int:pk>/",login_required(views.AgentView.as_view()),name="agent"),


    path("properties/",login_required(views.PropertiesView.as_view()),name="properties"),
    path("property/<int:pk>/",login_required(views.PropertyView.as_view()),name="property"),
    path("add_property/",login_required(apis.AddPropertyApi.as_view()),name="add_property"),
    
]
