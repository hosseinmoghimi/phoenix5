from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews.as_view(),name="home"),
    path('profile/<int:pk>/',views.ProfileViews.as_view(),name="profile"),
    path('logout/',views.LogoutViews.as_view(),name="logout"),
    path('membership_requests_app/<app_name>/',views.LogoutViews.as_view(),name="membership_requests_app"),
]
