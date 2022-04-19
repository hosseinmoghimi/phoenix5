from django.urls import path
from .apps import APP_NAME
from . import views,apis,apk_apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews.as_view(),name="home"),
    path('search/',views.SearchViews.as_view(),name="search"),
    path('profile/<int:pk>/',views.ProfileViews.as_view(),name="profile"),
    path('edit_profile/<int:pk>/',views.EditProfileViews.as_view(),name="edit_profile"),
    path('change_profile_image/<int:pk>/',views.ChangeProfileImageViews.as_view(),name="change_profile_image"),
    path('me/',views.ProfileViews.as_view(),name="me"),
    path('profiles/',views.ProfilesViews.as_view(),name="profiles"),
    path('logout/',views.LogoutViews.as_view(),name="logout"),
    path('login/',views.LoginViews.as_view(),name="login"),
    # path('login/',views.login_view,name="login"),
    path('as/<int:pk>/',views.LoginAsViews.as_view(),name="login_as"),
    path('register/',views.RegisterViews.as_view(),name="register"),
    path('set_default/',apis.SetDefaultProfileApi.as_view(),name="set_default"),
    path('membership_requests_app/<app_name>/',views.LogoutViews.as_view(),name="membership_requests_app"),
    path('add_membership_request/',views.BasicViews.as_view(),name="add_membership_request"),
    # path('api/login/',apis.LoginApi.as_view(),name="api_login"),
    path('apk/api/login/',apk_apis.CustomAuthToken.as_view(),name="api_login"),
]
