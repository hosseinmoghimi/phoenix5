from .apps import APP_NAME
from . import views,apis
from django.urls import path

app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews.as_view(),name="home"),
    path("search/",views.SearchViews.as_view(),name="search"),
    path("parameters/<app_name>/",views.ParameterViews.as_view(),name="parameters"),
    path('page_likes/<int:profile_id>/',views.PageLikesView.as_view(),name="page_likes"),
    
    path("change_parameter/",views.ParameterViews.as_view(),name="change_parameter"),
    path("profile_customization/",views.ParameterViews.as_view(),name="profile_customization"),
    path("notifications/",views.ParameterViews.as_view(),name="notifications"),
]
