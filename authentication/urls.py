from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews.as_view(),name="home"),
    path('search/',views.SearchViews.as_view(),name="search"),
    path('profile/<int:pk>/',views.ProfileViews.as_view(),name="profile"),
    path('edit_profile/<int:pk>/',views.EditProfileViews.as_view(),name="edit_profile"),
    path('me/',views.ProfileViews.as_view(),name="me"),
    path('profiles/',views.ProfilesViews.as_view(),name="profiles"),
    path('logout/',views.LogoutViews.as_view(),name="logout"),
    path('login/',views.LoginViews.as_view(),name="login"),
    # path('login/',views.login_view,name="login"),
    path('as/<int:pk>/',views.LoginAsViews.as_view(),name="login_as"),
    path('register/',views.RegisterViews.as_view(),name="register"),
    path('set_default/',apis.SetDefaultProfileApi.as_view(),name="set_default"),
    path('membership_requests_app/<app_name>/',views.LogoutViews.as_view(),name="membership_requests_app"),
]
