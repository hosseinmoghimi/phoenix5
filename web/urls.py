from .apps import APP_NAME
from django.urls import path
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("add_blog/",views.HomeView.as_view(),name="add_blog"),

    path("blog/<int:pk>/",views.BlogView.as_view(),name="blog"),
    path("feature/<int:pk>/",views.FeatureView.as_view(),name="feature"),
    path("our_work/<int:pk>/",views.OurWorkView.as_view(),name="ourwork"),
    path("our_team/<int:pk>/",views.HomeView.as_view(),name="ourteam"),
]
